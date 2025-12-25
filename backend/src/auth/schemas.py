"""
Pydantic schemas for authentication requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Optional


class BackgroundType(str, Enum):
    """User's professional background type."""
    SOFTWARE = "software"
    HARDWARE = "hardware"


# Request Schemas

class SignUpRequest(BaseModel):
    """Request schema for user signup."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    background: BackgroundType

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "background": "software"
            }
        }


class SignInRequest(BaseModel):
    """Request schema for user signin."""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UpdatePreferenceRequest(BaseModel):
    """Request schema for updating user preference."""
    background: BackgroundType

    class Config:
        json_schema_extra = {
            "example": {
                "background": "hardware"
            }
        }


# Response Schemas

class UserResponse(BaseModel):
    """Response schema for user data."""
    id: UUID
    email: str
    background: BackgroundType
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Response schema for authentication operations."""
    user: UserResponse
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "background": "software",
                    "created_at": "2025-12-25T10:00:00Z"
                },
                "message": "Successfully signed in"
            }
        }


class SessionResponse(BaseModel):
    """Response schema for session check."""
    authenticated: bool
    user: Optional[UserResponse] = None

    class Config:
        json_schema_extra = {
            "example": {
                "authenticated": True,
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "background": "software",
                    "created_at": "2025-12-25T10:00:00Z"
                }
            }
        }


class PreferenceResponse(BaseModel):
    """Response schema for user preference."""
    background: BackgroundType

    class Config:
        json_schema_extra = {
            "example": {
                "background": "software"
            }
        }


class ErrorDetail(BaseModel):
    """Error detail structure."""
    code: str
    message: str


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    error: ErrorDetail

    class Config:
        json_schema_extra = {
            "example": {
                "error": {
                    "code": "AUTH_INVALID_CREDENTIALS",
                    "message": "Invalid email or password"
                }
            }
        }
