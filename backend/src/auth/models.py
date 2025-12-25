"""
SQLAlchemy models for authentication.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.base_class import Base
import uuid
import enum


class BackgroundType(str, enum.Enum):
    """User's professional background type."""
    SOFTWARE = "software"
    HARDWARE = "hardware"


class User(Base):
    """User model for authentication and preferences."""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    background = Column(SQLEnum(BackgroundType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to sessions
    sessions = relationship("AuthSession", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', background='{self.background}')>"


class AuthSession(Base):
    """Session model for tracking user authentication sessions."""
    __tablename__ = "auth_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to user
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<AuthSession(id='{self.id}', user_id='{self.user_id}', expires_at='{self.expires_at}')>"
