# Implementation Plan: Better Auth Signup with User Background Preferences

**Branch**: `009-better-auth-signup` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-better-auth-signup/spec.md`

## Summary

Implement user authentication using Better Auth library with email/password signup that collects user background preferences (Software Developer / Hardware Engineer). The authentication system will integrate with the existing Docusaurus frontend and FastAPI backend, replacing localStorage-based preferences with server-side user profiles for cross-device persistence.

## Technical Context

**Language/Version**: TypeScript 5.x (Frontend), Python 3.11 (Backend)
**Primary Dependencies**:
- Frontend: Better Auth client, React 18, Docusaurus 3.x
- Backend: FastAPI, better-auth Python adapter, SQLAlchemy, Pydantic
**Storage**: Neon PostgreSQL (existing), new tables for users/sessions
**Testing**: Jest/React Testing Library (frontend), pytest (backend)
**Target Platform**: Web (Docusaurus static site + FastAPI API)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Authentication response < 500ms, session validation < 100ms
**Constraints**: Must integrate with existing personalization system, fallback to localStorage for unauthenticated users
**Scale/Scope**: Thousands of concurrent users, single-tenant application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Article | Requirement | Status | Notes |
|---------|-------------|--------|-------|
| I - Library-First | Auth as separate module | ✅ PASS | Auth will be a separate service module |
| II - Spec-Driven | Specs before code | ✅ PASS | Full spec created before planning |
| III - Documentation | Public API documented | ✅ PASS | OpenAPI contracts will be generated |
| IV - Content Standard | Static site preserved | ✅ PASS | Auth is dynamic, isolated from static content |
| V - Privacy/Security | No plaintext passwords | ✅ PASS | Better Auth handles secure hashing |
| V - Privacy/Security | Secrets in env vars | ✅ PASS | All secrets via environment variables |
| V - Privacy/Security | Input validation | ✅ PASS | Pydantic validation on all inputs |
| VI - Reusable Skills | Modular design | ✅ PASS | Auth context as reusable hook |
| VII - Personalization | User-level personalization | ✅ PASS | Core feature requirement |
| VIII - Simplicity | Limit projects (3-4 max) | ✅ PASS | Adding to existing backend/frontend |

**Gate Result**: ✅ PASS - No violations

## Project Structure

### Documentation (this feature)

```text
specs/009-better-auth-signup/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── auth-api.yaml    # OpenAPI spec for auth endpoints
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── auth/                    # NEW: Authentication module
│   │   ├── __init__.py
│   │   ├── router.py            # Auth API endpoints
│   │   ├── service.py           # Auth business logic
│   │   ├── models.py            # User/Session models
│   │   └── better_auth.py       # Better Auth integration
│   ├── models/
│   │   └── db_models.py         # MODIFY: Add User table
│   ├── services/
│   │   └── rag_service.py       # MODIFY: Use authenticated user preference
│   └── config.py                # MODIFY: Add auth config
└── tests/
    └── unit/
        └── test_auth.py         # NEW: Auth tests

docusaurus-book-site/
├── src/
│   ├── auth/                    # NEW: Auth client module
│   │   ├── AuthContext.tsx      # Auth state provider
│   │   ├── AuthProvider.tsx     # Better Auth client wrapper
│   │   └── useAuth.ts           # Auth hook
│   ├── components/
│   │   ├── Auth/                # NEW: Auth UI components
│   │   │   ├── SignUpForm.tsx
│   │   │   ├── SignInForm.tsx
│   │   │   ├── UserMenu.tsx
│   │   │   └── ProfileSettings.tsx
│   │   └── ChapterToolbar/
│   │       └── PersonalizeButton.tsx  # MODIFY: Use auth context
│   ├── hooks/
│   │   └── useUserPreferences.ts      # MODIFY: Integrate with auth
│   └── pages/
│       ├── auth/
│       │   ├── signin.tsx       # NEW: Sign in page
│       │   └── signup.tsx       # NEW: Sign up page
│       └── profile.tsx          # NEW: Profile/settings page
└── tests/
    └── auth/
        └── auth.test.tsx        # NEW: Auth component tests
```

**Structure Decision**: Web application structure - adding auth module to existing backend and frontend projects. No new top-level projects needed, maintaining constitution Article VIII compliance.

## Complexity Tracking

> No violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
