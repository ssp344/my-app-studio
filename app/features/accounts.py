"""Signup, login, private dashboard, and revocable cookie sessions."""

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app import security
from app.schemas import LoginInput, PublicUser, SignupInput

router = APIRouter()


def _render(request, template, context=None, status_code=200):
    """Render a form with a token and preserve any freshly issued cookie."""
    cookie_response = Response()
    token = security.csrf_token(request, cookie_response)
    response = request.app.state.templates.TemplateResponse(
        request=request,
        name=template,
        context={"csrf_token": token, **(context or {})},
        status_code=status_code,
    )
    for key, value in cookie_response.raw_headers:
        if key == b"set-cookie":
            response.raw_headers.append((key, value))
    return response


@router.get("/api/csrf")
def api_csrf(request: Request, response: Response):
    """Get the synchronizer token for same-origin JSON requests."""
    return {"csrf_token": security.csrf_token(request, response)}


@router.post("/api/signup", response_model=PublicUser, status_code=201)
def api_signup(
    credentials: SignupInput,
    request: Request,
    csrf: str | None = Header(default=None, alias="X-CSRF-Token"),
):
    """Create a member, rejecting extra fields such as a requested role."""
    security.require_csrf(request, csrf)
    security.limit_signup(request)
    return security.signup(
        request.app.state.settings, credentials.username, credentials.password
    )


@router.post("/api/login", response_model=PublicUser)
def api_login(
    credentials: LoginInput,
    request: Request,
    response: Response,
    csrf: str | None = Header(default=None, alias="X-CSRF-Token"),
):
    """Authenticate and rotate the session into a signed HttpOnly cookie."""
    security.require_csrf(request, csrf)
    return security.login(request, response, credentials.username, credentials.password)


@router.get("/api/me", response_model=PublicUser)
def api_me(user: dict = Depends(security.require_user)):
    """Return only the authenticated user's public identity fields."""
    return user


@router.post("/api/logout")
def api_logout(
    request: Request,
    response: Response,
    csrf: str | None = Header(default=None, alias="X-CSRF-Token"),
):
    """Revoke server state as well as removing the browser cookie."""
    security.require_csrf(request, csrf)
    security.logout(request, response)
    return {"message": "Logged out."}


@router.get("/signup", include_in_schema=False)
def signup_page(request: Request):
    """Show the reader registration form."""
    return _render(request, "account.html", {"signup": True})


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    """Show the reader sign-in form."""
    return _render(request, "account.html", {"signup": False})


async def _submit(request, signup):
    """Share bounded HTML validation without echoing rejected passwords."""
    username = ""
    try:
        async with request.form(max_fields=3, max_files=0, max_part_size=4096) as form:
            security.require_csrf(request, form.get("csrf_token"))
            data = {key: value for key, value in form.items() if key != "csrf_token"}
            if len(form.multi_items()) != len(form):
                raise HTTPException(422, "Please submit each field once.")
            credentials = (SignupInput if signup else LoginInput).model_validate(data)
        username = credentials.username
        response = RedirectResponse(
            "/login" if signup else "/dashboard", status_code=303
        )
        if signup:
            security.limit_signup(request)
            security.signup(
                request.app.state.settings, credentials.username, credentials.password
            )
        else:
            security.login(
                request, response, credentials.username, credentials.password
            )
        return response
    except ValidationError:
        error = "Check your username and password requirements below."
        status = 422
        headers = {}
    except HTTPException as exc:
        error, status, headers = exc.detail, exc.status_code, exc.headers or {}
    response = _render(
        request,
        "account.html",
        {"signup": signup, "error": error, "username": username},
        status_code=status,
    )
    response.headers.update(headers)
    return response


@router.post("/signup", include_in_schema=False)
async def signup_form(request: Request):
    """Create a reader account through the same guarded service as the API."""
    return await _submit(request, signup=True)


@router.post("/login", include_in_schema=False)
async def login_form(request: Request):
    """Sign in through the same guarded service as the API."""
    return await _submit(request, signup=False)


@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request):
    """Enforce authentication on the server before rendering private content."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return _render(request, "dashboard.html", {"user": user})


@router.post("/logout", include_in_schema=False)
async def logout_form(request: Request):
    """Require CSRF and revoke the session before returning to the homepage."""
    async with request.form(max_fields=1, max_files=0, max_part_size=4096) as form:
        security.require_csrf(request, form.get("csrf_token"))
    response = RedirectResponse("/", status_code=303)
    security.logout(request, response)
    return response
