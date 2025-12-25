# Tasks: Better Auth Signup with User Background Preferences

**Input**: Design documents from `/specs/009-better-auth-signup/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification. Test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `docusaurus-book-site/src/`
- Backend auth module: `backend/src/auth/`
- Frontend auth module: `docusaurus-book-site/src/auth/`
- Frontend components: `docusaurus-book-site/src/components/Auth/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependencies

- [x] T001 Add auth dependencies to backend/requirements.txt (passlib[bcrypt], python-jose[cryptography])
- [x] T002 Add better-auth dependency to docusaurus-book-site/package.json
- [x] T003 [P] Add auth environment variables to backend/.env.example (AUTH_SECRET_KEY, AUTH_SESSION_DURATION_DAYS, AUTH_COOKIE_SECURE, AUTH_COOKIE_SAMESITE)
- [x] T004 [P] Create backend/src/auth/__init__.py module structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create BackgroundType enum in backend/src/auth/models.py
- [x] T006 Create User SQLAlchemy model in backend/src/auth/models.py
- [x] T007 Create Session SQLAlchemy model in backend/src/auth/models.py
- [x] T008 Create database migration for users and sessions tables in backend/alembic/versions/
- [x] T009 Run database migration to create auth tables
- [x] T010 [P] Create Pydantic request/response schemas in backend/src/auth/schemas.py (SignUpRequest, SignInRequest, UserResponse, AuthResponse, SessionResponse, ErrorResponse)
- [x] T011 [P] Add auth configuration to backend/src/config.py (AUTH_SECRET_KEY, session settings, cookie settings)
- [x] T012 Create AuthService class with password hashing utilities in backend/src/auth/service.py
- [x] T013 Create session management methods in backend/src/auth/service.py (create_session, validate_session, invalidate_session)
- [x] T014 Create AuthContext.tsx in docusaurus-book-site/src/auth/AuthContext.tsx
- [x] T015 Create useAuth hook in docusaurus-book-site/src/auth/useAuth.ts
- [x] T016 Create AuthProvider wrapper in docusaurus-book-site/src/auth/AuthProvider.tsx
- [x] T017 Integrate AuthProvider into docusaurus-book-site/src/theme/Root.tsx (wrap app)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - New User Signup with Background Selection (Priority: P1) 🎯 MVP

**Goal**: Enable new visitors to create accounts with email, password, and background preference selection

**Independent Test**: Complete the signup form with background selection and verify the user account is created with preferences stored

### Implementation for User Story 1

- [x] T018 [US1] Implement signup method in backend/src/auth/service.py (create user with hashed password and background)
- [x] T019 [US1] Create POST /signup endpoint in backend/src/auth/router.py
- [x] T020 [US1] Add email uniqueness validation in backend/src/auth/service.py
- [x] T021 [US1] Add password strength validation (min 8 chars) in backend/src/auth/schemas.py
- [x] T022 [US1] Create SignUpForm component in docusaurus-book-site/src/components/Auth/SignUpForm.tsx
- [x] T023 [US1] Add background preference selector (Software/Hardware radio buttons) to SignUpForm
- [x] T024 [US1] Add form validation (email format, password length, background required) to SignUpForm
- [x] T025 [US1] Implement signup API call in useAuth hook
- [x] T026 [US1] Create signup page in docusaurus-book-site/src/pages/auth/signup.tsx
- [x] T027 [US1] Add "Sign Up" link to site header/navigation in docusaurus-book-site/src/theme/Navbar/
- [x] T028 [US1] Display welcome message with selected background after successful signup
- [x] T029 [US1] Handle signup errors (email exists, validation failures) with user-friendly messages

**Checkpoint**: User Story 1 complete - new users can sign up with background selection

---

## Phase 4: User Story 2 - Existing User Sign In (Priority: P1)

**Goal**: Enable returning users to sign in and load their stored background preference

**Independent Test**: Sign in with valid credentials and verify the user's stored background preference is loaded

### Implementation for User Story 2

- [x] T030 [US2] Implement signin method in backend/src/auth/service.py (validate credentials, create session)
- [x] T031 [US2] Create POST /signin endpoint in backend/src/auth/router.py
- [x] T032 [US2] Set HTTP-only session cookie on successful signin in backend/src/auth/router.py
- [x] T033 [US2] Create GET /session endpoint in backend/src/auth/router.py (validate session, return user data)
- [x] T034 [US2] Create SignInForm component in docusaurus-book-site/src/components/Auth/SignInForm.tsx
- [x] T035 [US2] Implement signin API call in useAuth hook
- [x] T036 [US2] Create signin page in docusaurus-book-site/src/pages/auth/signin.tsx
- [x] T037 [US2] Add "Sign In" link to site header/navigation
- [x] T038 [US2] Implement session check on app load in AuthProvider (call GET /session)
- [x] T039 [US2] Display generic error for invalid credentials (security: don't reveal which field is wrong)
- [x] T040 [US2] Modify useUserPreferences hook in docusaurus-book-site/src/hooks/useUserPreferences.ts to check auth state first

**Checkpoint**: User Stories 1 AND 2 complete - users can sign up and sign in

---

## Phase 5: User Story 3 - Sign Out (Priority: P2)

**Goal**: Enable signed-in users to sign out and terminate their session

**Independent Test**: Sign out and verify session is cleared and personalization reverts to localStorage fallback

### Implementation for User Story 3

- [x] T041 [US3] Implement signout method in backend/src/auth/service.py (invalidate session)
- [x] T042 [US3] Create POST /signout endpoint in backend/src/auth/router.py
- [x] T043 [US3] Clear session cookie on signout response
- [x] T044 [US3] Implement signout API call in useAuth hook
- [x] T045 [US3] Create UserMenu component in docusaurus-book-site/src/components/Auth/UserMenu.tsx (shows user email, sign out button)
- [x] T046 [US3] Add UserMenu to site header when user is authenticated
- [x] T047 [US3] Clear auth state in AuthContext on signout
- [x] T048 [US3] Ensure useUserPreferences falls back to localStorage after signout

**Checkpoint**: User Stories 1, 2, AND 3 complete - full auth flow working

---

## Phase 6: User Story 4 - Update Background Preference (Priority: P2)

**Goal**: Enable signed-in users to change their background preference in profile settings

**Independent Test**: Change preference in profile settings and verify personalized content reflects the new choice

### Implementation for User Story 4

- [x] T049 [US4] Implement update_preference method in backend/src/auth/service.py
- [x] T050 [US4] Create GET /user/preference endpoint in backend/src/auth/router.py
- [x] T051 [US4] Create PUT /user/preference endpoint in backend/src/auth/router.py
- [x] T052 [US4] Create ProfileSettings component in docusaurus-book-site/src/components/Auth/ProfileSettings.tsx
- [x] T053 [US4] Display current background preference with change option in ProfileSettings
- [x] T054 [US4] Implement updatePreference API call in useAuth hook
- [x] T055 [US4] Create profile page in docusaurus-book-site/src/pages/profile.tsx
- [x] T056 [US4] Add "Profile" link to UserMenu for authenticated users
- [x] T057 [US4] Update AuthContext state when preference is changed

**Checkpoint**: User Stories 1-4 complete - users can manage their preferences

---

## Phase 7: User Story 5 - Seamless Migration from localStorage (Priority: P3)

**Goal**: Migrate existing localStorage preferences to new user accounts during signup

**Independent Test**: Set localStorage preference, sign up, and verify the preference is transferred to the new account

### Implementation for User Story 5

- [x] T058 [US5] Check for existing localStorage preference in SignUpForm on mount
- [x] T059 [US5] Pre-populate background selector with localStorage value if found
- [x] T060 [US5] Add option to use existing preference or select new one in signup flow
- [x] T061 [US5] Clear localStorage preference after successful signup with migration
- [x] T062 [US5] Update useUserPreferences to handle migration state

**Checkpoint**: All user stories complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T063 [P] Register auth router in backend/src/main.py (mount at /api/auth)
- [x] T064 [P] Add CORS configuration for auth endpoints in backend/src/main.py
- [x] T065 [P] Create CSS styles for auth forms in docusaurus-book-site/src/components/Auth/Auth.module.css
- [x] T066 Handle session expiry gracefully (prompt re-login without losing content)
- [x] T067 Handle auth service unavailability (fallback to localStorage with notification)
- [x] T068 Add loading states to auth forms and buttons
- [x] T069 Verify all password handling is secure (no logging, proper hashing)
- [x] T070 Run quickstart.md validation (test all auth endpoints)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
- **Polish (Phase 8)**: Can start after Phase 2, some tasks depend on user stories

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1, but typically done after
- **User Story 3 (P2)**: Depends on US2 (need signin to test signout)
- **User Story 4 (P2)**: Depends on US2 (need authenticated user to update preference)
- **User Story 5 (P3)**: Depends on US1 (extends signup flow)

### Within Each User Story

- Backend implementation before frontend
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004 can run in parallel (different files)
- T010, T011 can run in parallel (different files)
- T063, T064, T065 can run in parallel (different files)
- Backend and frontend tasks within same story can be parallelized with coordination

---

## Parallel Example: Foundational Phase

```bash
# Launch parallel backend tasks:
Task: "Create Pydantic schemas in backend/src/auth/schemas.py"
Task: "Add auth configuration to backend/src/config.py"

# Launch parallel frontend tasks:
Task: "Create AuthContext.tsx"
Task: "Create useAuth hook"
Task: "Create AuthProvider wrapper"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Signup)
4. Complete Phase 4: User Story 2 (Signin)
5. **STOP and VALIDATE**: Test signup → signin → verify preference loaded
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test signup independently → Demo
3. Add User Story 2 → Test signin independently → Demo (MVP!)
4. Add User Story 3 → Test signout → Demo
5. Add User Story 4 → Test preference update → Demo
6. Add User Story 5 → Test localStorage migration → Demo
7. Complete Polish phase → Final release

### Single Developer Strategy

Execute phases sequentially in priority order:
1. Setup → Foundational → US1 → US2 → US3 → US4 → US5 → Polish

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Session cookies require HTTPS in production (AUTH_COOKIE_SECURE=true)
- Better Auth patterns used for secure password handling
