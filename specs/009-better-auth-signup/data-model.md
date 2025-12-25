# Data Model: Better Auth Signup with User Background Preferences

**Feature**: 009-better-auth-signup
**Date**: 2025-12-25

## Entity Overview

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ id (PK)             │
│ email               │
│ password_hash       │
│ background          │
│ created_at          │
│ updated_at          │
└─────────┬───────────┘
          │
          │ 1:N
          │
┌─────────▼───────────┐
│      Session        │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ token               │
│ expires_at          │
│ created_at          │
└─────────────────────┘
```

## Entities

### User

Represents a registered user with authentication credentials and personalization preferences.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (login identifier) |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| background | ENUM | NOT NULL | User's professional background ('software' or 'hardware') |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_users_email` on `email` (for login lookups)

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Email must be unique (case-insensitive)
- Password must be at least 8 characters before hashing
- Background must be one of: 'software', 'hardware'

---

### Session

Represents an active authentication session linking a user to a browser/device.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique session identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Reference to authenticated user |
| token | VARCHAR(255) | UNIQUE, NOT NULL | Secure session token (stored in HTTP-only cookie) |
| expires_at | TIMESTAMP | NOT NULL | Session expiration timestamp |
| created_at | TIMESTAMP | DEFAULT NOW() | Session creation timestamp |

**Indexes**:
- `idx_sessions_token` on `token` (for session validation)
- `idx_sessions_user_id` on `user_id` (for user session lookup)
- `idx_sessions_expires_at` on `expires_at` (for cleanup queries)

**Validation Rules**:
- Token must be cryptographically secure random string
- expires_at must be in the future at creation time
- On delete user cascade: delete all user sessions

**State Transitions**:
```
Created → Active → Expired/Invalidated
         ↓
      Signed Out
```

---

## Relationships

| From | To | Cardinality | Description |
|------|-----|-------------|-------------|
| User | Session | 1:N | A user can have multiple active sessions (different devices) |

---

## Enumerations

### BackgroundType

```python
class BackgroundType(str, Enum):
    SOFTWARE = "software"
    HARDWARE = "hardware"
```

---

## Database Migration

### Up Migration

```sql
-- Create background enum type
CREATE TYPE background_type AS ENUM ('software', 'hardware');

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    background background_type NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

### Down Migration

```sql
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS users;
DROP TYPE IF EXISTS background_type;
```

---

## SQLAlchemy Models

```python
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

class BackgroundType(str, enum.Enum):
    SOFTWARE = "software"
    HARDWARE = "hardware"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    background = Column(Enum(BackgroundType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="sessions")
```

---

## Pydantic Schemas

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from enum import Enum

class BackgroundType(str, Enum):
    SOFTWARE = "software"
    HARDWARE = "hardware"

# Request schemas
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    background: BackgroundType

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class UpdatePreferenceRequest(BaseModel):
    background: BackgroundType

# Response schemas
class UserResponse(BaseModel):
    id: UUID
    email: str
    background: BackgroundType
    created_at: datetime

class AuthResponse(BaseModel):
    user: UserResponse
    message: str

class SessionResponse(BaseModel):
    authenticated: bool
    user: UserResponse | None = None
```
