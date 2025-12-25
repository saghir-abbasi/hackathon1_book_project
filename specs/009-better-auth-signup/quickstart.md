# Quickstart Guide: Better Auth Signup with User Background Preferences

**Feature**: 009-better-auth-signup
**Date**: 2025-12-25

## Prerequisites

- Node.js 18+ (frontend)
- Python 3.11+ (backend)
- PostgreSQL database (Neon)
- Existing project setup with Docusaurus and FastAPI

## Environment Variables

Add these to your `.env` files:

### Backend (`backend/.env`)

```bash
# Existing variables...

# Auth Configuration
AUTH_SECRET_KEY=your-secret-key-min-32-chars
AUTH_SESSION_DURATION_DAYS=7
AUTH_COOKIE_SECURE=false  # Set to true in production
AUTH_COOKIE_SAMESITE=lax
```

### Frontend (`docusaurus-book-site/.env`)

```bash
# Existing variables...

# Auth API Base URL (same as existing API)
REACT_APP_AUTH_API_URL=http://localhost:8000/api/auth
```

## Database Setup

Run the migration to create auth tables:

```bash
cd backend
alembic upgrade head
```

Or manually execute the SQL:

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

## Backend Dependencies

Add to `backend/requirements.txt`:

```
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
```

Install:

```bash
cd backend
pip install -r requirements.txt
```

## Frontend Dependencies

Add to `docusaurus-book-site/package.json`:

```bash
cd docusaurus-book-site
npm install better-auth
```

## Quick Verification

### 1. Start Backend

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend

```bash
cd docusaurus-book-site
npm start
```

### 3. Test Auth Endpoints

```bash
# Sign up
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","background":"software"}'

# Sign in
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# Get session
curl -X GET http://localhost:8000/api/auth/session \
  -b cookies.txt

# Sign out
curl -X POST http://localhost:8000/api/auth/signout \
  -b cookies.txt
```

## Integration Points

### Existing useUserPreferences Hook

The auth system integrates with the existing `useUserPreferences` hook:

```typescript
// Before (localStorage only)
const { background } = useUserPreferences();

// After (auth-aware, falls back to localStorage)
const { background, isAuthenticated, user } = useUserPreferences();
```

### Chapter Personalization

No changes needed - the personalization system automatically uses the authenticated user's background preference when available.

## Common Issues

### Session not persisting

- Ensure `AUTH_COOKIE_SECURE=false` for localhost
- Check that cookies are being sent with credentials

### CORS errors

- Verify `CORS_ORIGINS` in backend includes frontend URL
- Ensure credentials mode is enabled in fetch requests

### Password hash errors

- Ensure `passlib[bcrypt]` is installed correctly
- On Windows, may need to install `bcrypt` separately

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement backend auth module
3. Implement frontend auth components
4. Test integration with existing personalization system
