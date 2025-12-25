"""
Authentication service with password hashing and session management.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID
import secrets

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .models import User, AuthSession, BackgroundType
from .schemas import SignUpRequest, UserResponse
from ..config import settings


# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthError(Exception):
    """Base exception for authentication errors."""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class AuthService:
    """Service class for authentication operations."""

    def __init__(self, db: Session):
        self.db = db

    # Password utilities

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_session_token() -> str:
        """Generate a cryptographically secure session token."""
        return secrets.token_urlsafe(32)

    # User operations

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address."""
        return self.db.query(User).filter(User.email == email.lower()).first()

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by their ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, signup_data: SignUpRequest) -> User:
        """
        Create a new user with hashed password.

        Raises:
            AuthError: If email already exists
        """
        # Check if email already exists
        existing_user = self.get_user_by_email(signup_data.email)
        if existing_user:
            raise AuthError("AUTH_EMAIL_EXISTS", "Email already registered")

        # Create new user
        user = User(
            email=signup_data.email.lower(),
            password_hash=self.hash_password(signup_data.password),
            background=BackgroundType(signup_data.background.value)
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticate a user with email and password.

        Raises:
            AuthError: If credentials are invalid
        """
        user = self.get_user_by_email(email)

        if not user or not self.verify_password(password, user.password_hash):
            # Use generic error message for security
            raise AuthError("AUTH_INVALID_CREDENTIALS", "Invalid email or password")

        return user

    def update_user_preference(self, user_id: UUID, background: BackgroundType) -> User:
        """
        Update a user's background preference.

        Raises:
            AuthError: If user not found
        """
        user = self.get_user_by_id(user_id)

        if not user:
            raise AuthError("AUTH_USER_NOT_FOUND", "User not found")

        user.background = background
        self.db.commit()
        self.db.refresh(user)

        return user

    # Session management

    def create_session(self, user: User) -> AuthSession:
        """Create a new session for a user."""
        token = self.generate_session_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.AUTH_SESSION_DURATION_DAYS)

        session = AuthSession(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def validate_session(self, token: str) -> Optional[User]:
        """
        Validate a session token and return the associated user.

        Returns:
            User if session is valid and not expired, None otherwise
        """
        session = self.db.query(AuthSession).filter(AuthSession.token == token).first()

        if not session:
            return None

        # Check if session has expired
        if session.expires_at < datetime.now(timezone.utc):
            # Clean up expired session
            self.db.delete(session)
            self.db.commit()
            return None

        return session.user

    def invalidate_session(self, token: str) -> bool:
        """
        Invalidate a session token (sign out).

        Returns:
            True if session was found and deleted, False otherwise
        """
        session = self.db.query(AuthSession).filter(AuthSession.token == token).first()

        if not session:
            return False

        self.db.delete(session)
        self.db.commit()

        return True

    def invalidate_all_user_sessions(self, user_id: UUID) -> int:
        """
        Invalidate all sessions for a user.

        Returns:
            Number of sessions deleted
        """
        result = self.db.query(AuthSession).filter(AuthSession.user_id == user_id).delete()
        self.db.commit()

        return result

    def cleanup_expired_sessions(self) -> int:
        """
        Clean up all expired sessions.

        Returns:
            Number of sessions deleted
        """
        result = self.db.query(AuthSession).filter(
            AuthSession.expires_at < datetime.now(timezone.utc)
        ).delete()
        self.db.commit()

        return result
