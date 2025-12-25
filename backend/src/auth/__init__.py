"""
Authentication module for the Book Project.

This module provides user authentication functionality including:
- User signup with background preference
- User signin with session management
- Session validation and signout
- User preference management
"""

from .models import User, AuthSession, BackgroundType
from .schemas import (
    SignUpRequest,
    SignInRequest,
    UserResponse,
    AuthResponse,
    SessionResponse,
    PreferenceResponse,
    UpdatePreferenceRequest,
    ErrorResponse,
)
from .service import AuthService
from .router import router as auth_router

__all__ = [
    "User",
    "AuthSession",
    "BackgroundType",
    "SignUpRequest",
    "SignInRequest",
    "UserResponse",
    "AuthResponse",
    "SessionResponse",
    "PreferenceResponse",
    "UpdatePreferenceRequest",
    "ErrorResponse",
    "AuthService",
    "auth_router",
]
