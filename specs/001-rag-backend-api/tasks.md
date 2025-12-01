# Tasks: Backend API Layer (FastAPI + Qdrant + Neon)

**Input**: Design documents from `/specs/001-rag-backend-api/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml, quickstart.md

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`
- Paths shown below assume backend project structure.

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize the `backend/` folder and Python environment.

- [ ] T001 Create directory `backend/`
- [ ] T002 Initialize Python virtual environment inside `backend/`
- [ ] T003 Create `backend/requirements.txt` with initial dependencies: FastAPI, Uvicorn, Qdrant-client, Psycopg2-binary, SQLAlchemy, Pydantic, python-dotenv, openai/anthropic (choose one based on environment variable)
- [ ] T004 Create `backend/.env.example`
- [ ] T005 Create `backend/src/` directory
- [ ] T006 Create `backend/src/main.py`
- [ ] T007 Create `backend/src/config.py`
- [ ] T008 Create `backend/tests/` directory
- [ ] T009 Create `backend/Dockerfile`
- [ ] T010 Create `backend/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Set up FastAPI application, CORS, and basic configurations.

- [ ] T011 Initialize FastAPI app instance in `backend/src/main.py`
- [ ] T012 Implement `/health` endpoint in `backend/src/main.py`
- [ ] T013 Configure CORS for Docusaurus origin in `backend/src/main.py`
- [ ] T014 Implement environment variable loading in `backend/src/config.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Embed Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable embedding of book content chunks into Qdrant.

**Independent Test**: Provide book content chunks to the `/embed` endpoint and verify that embeddings are stored in Qdrant.

### Implementation for User Story 1

- [ ] T015 [P] [US1] Create `backend/src/db/` directory
- [ ] T016 [P] [US1] Create `backend/src/db/qdrant_client.py`
- [ ] T017 [US1] Implement Qdrant client connection in `backend/src/db/qdrant_client.py`
- [ ] T018 [US1] Implement function to create Qdrant collection (if not exists) in `backend/src/db/qdrant_client.py`
- [ ] T019 [US1] Implement function to upsert vectors in `backend/src/db/qdrant_client.py`
- [ ] T020 [P] [US1] Create `backend/src/core/` directory
- [ ] T021 [P] [US1] Create `backend/src/core/embeddings.py`
- [ ] T022 [US1] Implement text chunking logic in `backend/src/core/embeddings.py`
- [ ] T023 [US1] Implement embedding generation using OpenAI/Claude API in `backend/src/core/embeddings.py`
- [ ] T024 [US1] Implement data preparation for Qdrant upsert in `backend/src/core/embeddings.py`
- [ ] T025 [P] [US1] Create `backend/src/models/` directory
- [ ] T026 [P] [US1] Define Pydantic models for `/embed` request/response in `backend/src/models/embed_models.py`
- [ ] T027 [P] [US1] Create `backend/src/api/` directory
- [ ] T028 [US1] Implement `/embed` API endpoint in `backend/src/api/embed_router.py` (integrate into `main.py`)
- [ ] T029 [P] [US1] Create `backend/tests/unit/` directory
- [ ] T030 [US1] Write unit tests for `/embed` endpoint in `backend/tests/unit/test_embed.py`

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Query Book Content (Priority: P1)

**Goal**: Enable querying of book content chunks from Qdrant.

**Independent Test**: Send a user question to the `/query` endpoint and receive relevant text chunks from Qdrant.

### Implementation for User Story 2

- [ ] T031 [US2] Implement Qdrant vector search function in `backend/src/db/qdrant_client.py`
- [ ] T032 [P] [US2] Define Pydantic models for `/query` request/response in `backend/src/models/query_models.py`
- [ ] T033 [US2] Implement `/query` API endpoint in `backend/src/api/query_router.py` (integrate into `main.py`)
- [ ] T034 [US2] Write unit tests for `/query` endpoint in `backend/tests/unit/test_query.py`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Chat with RAG Chatbot (Priority: P1)

**Goal**: Enable full RAG chatbot interaction with assembled responses.

**Independent Test**: Send user input to the `/chat` endpoint and receive an assistant response based on retrieved context.

### Implementation for User Story 3

- [ ] T035 [P] [US3] Create `backend/src/services/` directory
- [ ] T036 [P] [US3] Create `backend/src/services/rag_service.py`
- [ ] T037 [US3] Implement logic to retrieve relevant segments using Qdrant client in `backend/src/services/rag_service.py`
- [ ] T038 [US3] Implement logic to assemble context and generate assistant response in `backend/src/services/rag_service.py`
- [ ] T039 [P] [US3] Define Pydantic models for `/chat` request/response in `backend/src/models/chat_models.py`
- [ ] T040 [US3] Implement `/chat` API endpoint in `backend/src/api/chat_router.py` (integrate into `main.py`)
- [ ] T041 [US3] Write unit tests for `/chat` endpoint in `backend/tests/unit/test_chat.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Manage Chat Sessions (Priority: P2)

**Goal**: Store and manage chat sessions and history in Neon PostgreSQL.

**Independent Test**: Verify user session data and chat history are stored and retrieved from the Neon PostgreSQL database after chat interactions.

### Implementation for User Story 4

- [ ] T042 [P] [US4] Create `backend/src/db/database.py` (if not already created)
- [ ] T043 [US4] Implement SQLAlchemy engine and session creation in `backend/src/db/database.py`
- [ ] T044 [P] [US4] Create `backend/src/models/db_models.py`
- [ ] T045 [US4] Define SQLAlchemy models for `UserSession` and `ChatMessage` in `backend/src/models/db_models.py`
- [ ] T046 [US4] Implement methods for creating database tables (additive) in `backend/src/db/database.py`
- [ ] T047 [US4] Implement database helper functions for inserting and retrieving session data in `backend/src/db/database.py`
- [ ] T048 [US4] Integrate session management into `/chat` endpoint in `backend/src/api/chat_router.py`
- [ ] T049 [US4] Write unit tests for database interactions in `backend/tests/unit/test_database.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finalize environment, security, and overall testing.

- [ ] T050 [P] Update `backend/.env.example` with all required environment variables
- [ ] T051 [P] Ensure all API keys/credentials are loaded securely via `backend/src/config.py`
- [ ] T052 [P] Update `backend/requirements.txt` with final dependencies for testing and production
- [ ] T053 [P] Implement a simple `Dockerfile` for the backend application (`backend/Dockerfile`)
- [ ] T054 [P] Create `backend/tests/integration/` directory
- [ ] T055 [P] Implement integration tests (Qdrant connectivity, Neon DB session creation, embedding generation, vector search) in `backend/tests/integration/test_integration.py`
- [ ] T056 [P] Create `backend/README.md` with setup and usage instructions
- [ ] T057 Run quickstart.md validation (manual step)
- [ ] T058 Manually verify all acceptance criteria from `spec.md` (manual step)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion. User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 -> P2).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1 - Embed Book Content)**: Can start after Foundational (Phase 2).
- **User Story 2 (P1 - Query Book Content)**: Can start after Foundational (Phase 2) and User Story 1.
- **User Story 3 (P1 - Chat with RAG Chatbot)**: Can start after Foundational (Phase 2), User Story 1, and User Story 2.
- **User Story 4 (P2 - Manage Chat Sessions)**: Can start after Foundational (Phase 2) and User Story 3.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation.
- Models before services.
- Services before endpoints.
- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- **Phase 1**: All tasks T001-T010 can run in parallel.
- **Phase 3**: T015, T016, T020, T021, T025, T026, T027, T029 can run in parallel.
- **Phase 4**: T032 can run in parallel with T031.
- **Phase 5**: T035, T036, T039 can run in parallel.
- **Phase 6**: T042, T044 can run in parallel.
- **Phase 7**: All tasks T050-T056 can run in parallel.

---

## Parallel Example: User Story 1 (Embed Book Content)

```bash
# Launch all parallel tasks for User Story 1 together:
- [P] T015 [US1] Create backend/src/db/ directory
- [P] T016 [US1] Create backend/src/db/qdrant_client.py
- [P] T020 [US1] Create backend/src/core/ directory
- [P] T021 [US1] Create backend/src/core/embeddings.py
- [P] T025 [US1] Create backend/src/models/ directory
- [P] T026 [US1] Define Pydantic models for /embed request/response in backend/src/models/embed_models.py
- [P] T027 [US1] Create backend/src/api/ directory
- [P] T029 [US1] Create backend/tests/unit/ directory
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Embed Book Content)
4.  Complete Phase 4: User Story 2 (Query Book Content)
5.  **STOP and VALIDATE**: Test User Story 1 and 2 independently and together.
6.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Add User Story 4 → Test independently → Deploy/Demo
6.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 1 & 2 (Embedding and Querying)
    -   Developer B: User Story 3 (Chat with RAG Chatbot)
    -   Developer C: User Story 4 (Manage Chat Sessions)
3.  Stories complete and integrate independently.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
