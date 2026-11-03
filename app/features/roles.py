"""Server-enforced admin permissions using the current database role."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app import security

router = APIRouter()


def _overview():
    """Keep the agreed admin result small and free of reader account data."""
    return {
        "message": "Welcome to the bookstore administration overview.",
        "store": "Shiv’s Book Store",
        "sample_books": 3,
        "catalog_status": "Demo shelf; ordering is not available.",
    }


@router.get("/api/admin")
def admin_api(_user: dict = Depends(security.require_admin)):
    """Require an authenticated admin even for direct API requests."""
    return _overview()


@router.get("/admin", include_in_schema=False)
def admin_page(request: Request):
    """Redirect anonymous users and deny members before rendering admin content."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    if user["role"] != "admin":
        return request.app.state.templates.TemplateResponse(
            request=request, name="forbidden.html", context={}, status_code=403
        )
    return request.app.state.templates.TemplateResponse(
        request=request, name="admin.html", context={"overview": _overview()}
    )
