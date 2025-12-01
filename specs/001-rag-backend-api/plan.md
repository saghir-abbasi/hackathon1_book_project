# Implementation Plan: Backend API Layer (FastAPI + Qdrant + Neon)

**Branch**: `001-rag-backend-api` | **Date**: 2025-12-01 | **Spec**: specs/001-rag-backend-api/spec.md
**Input**: Feature specification from `specs/001-rag-backend-api/spec.md`

## Summary

This plan details the development of a fully functional backend for the RAG chatbot using FastAPI, Qdrant for vector search, and Neon Serverless PostgreSQL for session management. The implementation will handle book content embedding, vector search, chat session management, and response assembly. All backend components will be developed in an isolated and additive manner within a dedicated `backend/` folder, ensuring no existing frontend code, project data, or git branches are altered.

## Technical Context

**Language/Version**: Python 3.9+ (compatible with FastAPI and required libraries)
**Primary Dependencies**: FastAPI, Uvicorn, Qdrant Client, Psycopg2-binary, SQLAlchemy, Pydantic, python-dotenv, OpenAI / Claude API client (for embeddings)
**Storage**: Qdrant (vector database for embeddings), Neon Serverless PostgreSQL (relational database for user sessions and chat history)
**Testing**: pytest
**Target Platform**: Linux server (containerized deployment is assumed)
**Project Type**: Backend API
**Performance Goals**:
  - `/embed` endpoint processes 100 book content chunks within 10 seconds (SC-001)
  - `/query` endpoint returns relevant text chunks for 90% of user questions within 1 second (SC-002)
  - `/chat` endpoint provides an assembled assistant response within 3 seconds for 95% of user inputs (SC-003)
  - User session data stored and retrieved from PostgreSQL in < 500ms (SC-005)
**Constraints**:
  - Isolated and additive implementation: No modification of existing frontend components, project files, or git branches.
  - No hard-coded credentials: All API keys, database URLs, and secrets stored in `.env` files.
  - CORS enabled for Docusaurus frontend integration.
**Scale/Scope**: Supports RAG chatbot for book content, handling multiple concurrent users and chat sessions.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **Article I (Library-First & Modular Design)**: ✅ PASS. The backend is designed as a separate, modular service within its own folder (`backend/`), promoting clear boundaries and reusability.
-   **Article II (Spec-Driven & Test-First Workflow)**: ✅ PASS. This plan is derived directly from a detailed specification, and includes unit testing in the plan.
-   **Article III (Documentation, Content & Code Quality Standards)**: ✅ PASS. The plan implies adherence to standard code quality, documentation practices, and unit testing.
-   **Article IV (Content & Deployment Standard)**: ✅ PASS. The backend API is entirely separate from the Docusaurus static site, maintaining content lightweightness and isolating dynamic behavior.
-   **Article V (RAG & AI Integrations: Privacy, Security & Data Handling)**: ✅ PASS. The plan explicitly addresses security by mandating `.env` for secrets and validating user inputs implicitly through API design.
-   **Article VI (Reusable Intelligence: Subagents & Agent Skills)**: N/A for this planning phase. This article is more relevant to subsequent implementation or refactoring phases.
-   **Article VII (Internationalization & Personalization Support)**: N/A for this planning phase. This article is not directly applicable to the core backend API layer for RAG.
-   **Article VIII (Simplicity & Minimalism)**: ✅ PASS. The plan outlines a focused backend API without unnecessary complexity or over-engineering, building for known requirements.
-   **Article IX (Version Control, Release & Traceability)**: ✅ PASS. The entire project (including this backend) is version-controlled with Git, ensuring traceability.

All constitutional gates pass.

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-backend-api/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/                 # FastAPI application and endpoints
│   ├── core/                # Core logic: RAG pipeline, chunking, embeddings
│   ├── db/                  # Database interaction (Qdrant, PostgreSQL)
│   ├── models/              # Pydantic models for request/response, DB schemas
│   └── services/            # Business logic and external service integrations
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── Dockerfile
├── requirements.txt
└── README.md
```

**Structure Decision**: The backend will reside in a new top-level `backend/` directory, separate from `docusaurus-book-site/`. This adheres to the isolation constraint and allows independent development and deployment. The internal structure of `backend/src/` is modular, reflecting logical components (API, core RAG logic, database, models, services).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

- None. All constitutional checks passed.