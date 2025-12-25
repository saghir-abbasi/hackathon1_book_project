# Research: Better Auth Signup with User Background Preferences

**Feature**: 009-better-auth-signup
**Date**: 2025-12-25

## Research Summary

This document captures research findings for implementing Better Auth authentication with user background preferences in the existing Docusaurus + FastAPI stack.

---

## 1. Better Auth Library Integration

### Decision: Use Better Auth with custom backend adapter

**Rationale**: Better Auth is a modern, TypeScript-first authentication library that provides:
- Built-in email/password authentication
- Session management with secure cookies
- React hooks for frontend integration
- Extensible plugin architecture for custom fields (background preference)

**Alternatives Considered**:

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| NextAuth.js | Popular, well-documented | Designed for Next.js, poor Docusaurus fit | Not compatible with static site architecture |
| Auth0 | Enterprise features, managed | External dependency, cost at scale | Over-engineered for simple email/password |
| Custom JWT | Full control | Security risks, maintenance burden | Violates Article VIII - reinventing wheel |
| Supabase Auth | PostgreSQL native | Requires Supabase infrastructure | Conflicts with existing Neon PostgreSQL |

**Implementation Approach**:
- Frontend: Use `better-auth/react` client SDK
- Backend: Create FastAPI adapter following Better Auth server patterns
- Storage: Use existing Neon PostgreSQL with new auth tables

---

## 2. Backend Integration Strategy

### Decision: Create dedicated auth module in FastAPI backend

**Rationale**:
- Keeps authentication logic isolated (Article I compliance)
- Reuses existing database connection and configuration
- Allows shared session validation across existing endpoints

**Key Components**:
1. **Auth Router** (`/api/auth/*`): Handles signup, signin, signout, session validation
2. **User Model**: SQLAlchemy model with email, password_hash, background preference
3. **Session Model**: Tracks active sessions with expiration
4. **Auth Service**: Business logic for credential validation, session management

**Password Security**:
- Use `passlib` with bcrypt hashing (industry standard)
- Better Auth patterns for secure password verification
- Never log or expose password hashes

---

## 3. Frontend Integration Strategy

### Decision: React Context with custom hook

**Rationale**:
- Consistent with existing `useUserPreferences` hook pattern
- Allows seamless integration with ChapterToolbar components
- Provides global auth state across all pages

**Implementation**:
1. **AuthProvider**: Wraps app at Root level, manages auth state
2. **useAuth hook**: Provides `user`, `isAuthenticated`, `signIn`, `signOut`, `signUp`
3. **Protected routes**: Optional, not needed for current feature scope

**Integration with Existing Code**:
- Modify `useUserPreferences` to check auth state first
- If authenticated: fetch preference from server
- If not authenticated: fall back to localStorage (existing behavior)

---

## 4. Database Schema Design

### Decision: Extend existing PostgreSQL with users and sessions tables

**Rationale**:
- Leverages existing Neon PostgreSQL connection
- Maintains data integrity with foreign keys
- Allows future expansion (roles, permissions)

**Tables**:
```sql
users (
  id: UUID PRIMARY KEY,
  email: VARCHAR UNIQUE NOT NULL,
  password_hash: VARCHAR NOT NULL,
  background: ENUM('software', 'hardware') NOT NULL,
  created_at: TIMESTAMP DEFAULT NOW(),
  updated_at: TIMESTAMP DEFAULT NOW()
)

sessions (
  id: UUID PRIMARY KEY,
  user_id: UUID REFERENCES users(id),
  token: VARCHAR UNIQUE NOT NULL,
  expires_at: TIMESTAMP NOT NULL,
  created_at: TIMESTAMP DEFAULT NOW()
)
```

---

## 5. Session Management

### Decision: HTTP-only cookies with server-side session storage

**Rationale**:
- More secure than localStorage/sessionStorage for tokens
- Protected against XSS attacks
- Automatic session handling by browser

**Session Flow**:
1. User signs in → Server creates session, sets HTTP-only cookie
2. Subsequent requests → Browser sends cookie, server validates session
3. Sign out → Server invalidates session, clears cookie
4. Expiration → Session auto-invalidated after configured duration

**Configuration**:
- Session duration: 7 days (configurable)
- Secure flag: true in production
- SameSite: Lax (allows navigation from external links)

---

## 6. Background Preference Integration

### Decision: Store preference in user table, sync on auth state change

**Rationale**:
- Single source of truth for authenticated users
- Immediate availability after sign in
- No separate API call needed

**Migration from localStorage**:
1. On signup: Check localStorage for existing preference
2. If found: Pre-populate signup form with existing preference
3. On successful signup: Clear localStorage, use server value
4. On sign out: Revert to localStorage-based behavior

---

## 7. Error Handling Strategy

### Decision: Structured error responses with user-friendly messages

**Rationale**:
- Consistent error format across all auth endpoints
- Security-conscious messages (don't reveal if email exists)
- Actionable feedback for users

**Error Response Format**:
```json
{
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

**Error Codes**:
- `AUTH_INVALID_CREDENTIALS`: Wrong email/password
- `AUTH_EMAIL_EXISTS`: Email already registered
- `AUTH_WEAK_PASSWORD`: Password doesn't meet requirements
- `AUTH_SESSION_EXPIRED`: Session has expired
- `AUTH_REQUIRED`: Authentication required for action

---

## 8. Testing Strategy

### Decision: Unit tests for auth logic, integration tests for API

**Backend Tests**:
- Password hashing/verification
- Session creation/validation
- User creation with preference
- Protected endpoint access

**Frontend Tests**:
- Auth context state management
- Form validation
- Integration with useUserPreferences
- UI component rendering

---

## Resolved Clarifications

| Original Unknown | Resolution | Source |
|------------------|------------|--------|
| Better Auth Python adapter | Create custom FastAPI adapter following Better Auth patterns | Architecture decision |
| Session storage mechanism | HTTP-only cookies with server-side session table | Security best practices |
| Preference migration | Check localStorage on signup, offer to use existing | UX consideration |
| Password requirements | Minimum 8 characters, handled by frontend validation | Industry standard |
