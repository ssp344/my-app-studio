"""The separate admin sign-in must not grant privileges to reader accounts."""

import re

from app import database


def test_admin_sign_in_respects_current_role(client, settings):
    """One login works only after trusted promotion, including direct admin APIs."""
    credentials = {"username": "role_reader", "password": "disposable test passphrase"}
    csrf = client.get("/api/csrf").json()["csrf_token"]
    assert (
        client.post(
            "/api/signup", json=credentials, headers={"X-CSRF-Token": csrf}
        ).status_code
        == 201
    )
    assert "/admin/login" in client.get("/login").text
    for role, expected in (("member", 403), ("admin", 200)):
        assert database.set_role(settings, credentials["username"], role)
        form = client.get("/admin/login")
        assert "Admin sign in" in form.text
        token = re.search(r'name="csrf_token" value="([^"]+)"', form.text).group(1)
        response = client.post(
            "/admin/login",
            data={**credentials, "csrf_token": token},
            follow_redirects=False,
        )
        assert response.status_code == 303
        assert response.headers["location"] == "/admin"
        assert client.get("/admin").status_code == expected
        assert client.get("/api/admin").status_code == expected
