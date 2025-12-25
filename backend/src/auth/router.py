"""
FastAPI router for authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from typing import Optional

from ..db.database import get_db
from ..config import settings
from .service import AuthService, AuthError
from .schemas import (
    SignUpRequest,
    SignInRequest,
    UpdatePreferenceRequest,
    AuthResponse,
    SessionResponse,
    PreferenceResponse,
    ErrorResponse,
    UserResponse,
)


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency to get AuthService instance."""
    return AuthService(db)


def get_current_user(
    session_token: Optional[str] = Cookie(None, alias=settings.AUTH_COOKIE_NAME),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Dependency to get current authenticated user from session cookie."""
    if not session_token:
        return None
    return auth_service.validate_session(session_token)


def require_auth(
    session_token: Optional[str] = Cookie(None, alias=settings.AUTH_COOKIE_NAME),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Dependency that requires authentication."""
    if not session_token:
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "AUTH_REQUIRED", "message": "Authentication required"}}
        )

    user = auth_service.validate_session(session_token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "AUTH_SESSION_EXPIRED", "message": "Session has expired"}}
        )

    return user


def set_session_cookie(response: Response, token: str):
    """Set the session cookie on the response."""
    response.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        max_age=settings.AUTH_SESSION_DURATION_DAYS * 24 * 60 * 60,  # Convert days to seconds
        path="/"
    )


def clear_session_cookie(response: Response):
    """Clear the session cookie."""
    response.delete_cookie(
        key=settings.AUTH_COOKIE_NAME,
        path="/"
    )


# =============================================================================
# User Story 1: Signup Endpoint
# =============================================================================

@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(
    request: SignUpRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user with email, password, and background preference.

    Creates a new user account and returns a session cookie for immediate authentication.
    """
    try:
        # Create the user
        user = auth_service.create_user(request)

        # Create a session for the new user
        session = auth_service.create_session(user)

        # Set the session cookie
        set_session_cookie(response, session.token)

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                background=user.background.value,
                created_at=user.created_at
            ),
            message=f"Welcome! Your account has been created with {user.background.value} background."
        )

    except AuthError as e:
        if e.code == "AUTH_EMAIL_EXISTS":
            raise HTTPException(
                status_code=409,
                detail={"error": {"code": e.code, "message": e.message}}
            )
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": e.code, "message": e.message}}
        )


# =============================================================================
# User Story 2: Signin & Session Endpoints
# =============================================================================

@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SignInRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Sign in an existing user with email and password.

    Returns user data and sets a session cookie.
    """
    try:
        # Authenticate the user
        user = auth_service.authenticate_user(request.email, request.password)

        # Create a session
        session = auth_service.create_session(user)

        # Set the session cookie
        set_session_cookie(response, session.token)

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                background=user.background.value,
                created_at=user.created_at
            ),
            message="Successfully signed in"
        )

    except AuthError as e:
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": e.code, "message": e.message}}
        )


@router.get("/session", response_model=SessionResponse)
async def get_session(
    user = Depends(get_current_user)
):
    """
    Check if user is authenticated and get user data.

    Returns authentication status and user data if authenticated.
    """
    if not user:
        return SessionResponse(authenticated=False, user=None)

    return SessionResponse(
        authenticated=True,
        user=UserResponse(
            id=user.id,
            email=user.email,
            background=user.background.value,
            created_at=user.created_at
        )
    )


# =============================================================================
# User Story 3: Signout Endpoint
# =============================================================================

@router.post("/signout")
async def signout(
    response: Response,
    session_token: Optional[str] = Cookie(None, alias=settings.AUTH_COOKIE_NAME),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Sign out the current user by invalidating their session.

    Clears the session cookie regardless of whether the session was found.
    """
    if session_token:
        auth_service.invalidate_session(session_token)

    # Always clear the cookie
    clear_session_cookie(response)

    return {"message": "Successfully signed out"}


# =============================================================================
# User Story 4: User Preference Endpoints
# =============================================================================

@router.get("/user/preference", response_model=PreferenceResponse)
async def get_preference(
    user = Depends(require_auth)
):
    """
    Get the authenticated user's background preference.
    """
    return PreferenceResponse(background=user.background.value)


@router.put("/user/preference", response_model=PreferenceResponse)
async def update_preference(
    request: UpdatePreferenceRequest,
    user = Depends(require_auth),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Update the authenticated user's background preference.
    """
    from .models import BackgroundType as ModelBackgroundType

    updated_user = auth_service.update_user_preference(
        user.id,
        ModelBackgroundType(request.background.value)
    )

    return PreferenceResponse(background=updated_user.background.value)
