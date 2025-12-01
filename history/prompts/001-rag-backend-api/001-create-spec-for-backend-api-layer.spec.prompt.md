---
id: 001
title: Create Spec for Backend API Layer
stage: spec
date: 2025-12-01
surface: agent
model: gemini-pro
feature: 001-rag-backend-api
branch: 001-rag-backend-api
user: User
command: /sp.specify "Feature: 2.3 — Backend API Layer (FastAPI + Qdrant + Neon) Objective: Develop the backend services for the RAG chatbot, including book content embedding, vector search, chat session handling, and database integration. All implementation must be **isolated and additive**, ensuring no existing frontend components, project files, or git branches are deleted or modified. Requirements: 1. FastAPI Server Setup - Create a new FastAPI project under a separate folder, e.g., `backend/`. - Implement the following API endpoints: • `/embed` — Accept book content chunks and store embeddings in Qdrant. • `/query` — Accept user questions and return relevant text chunks from Qdrant. • `/chat` — Accept user input, retrieve relevant context, and return assistant response. - Enable CORS for frontend Docusaurus integration. - **Do not modify any existing frontend components or files.** 2. Qdrant Vector Database Integration - Set up a Qdrant collection specifically for book embeddings. - Implement functions to: • `upsert` embeddings • `search` nearest neighbors for a query - Store connection credentials in a `.env` file. - **Ensure all work is isolated and additive, without touching previous project files.** 3. Neon Serverless PostgreSQL Integration - Create database tables for: • User sessions • Optional chat history for analytics - Implement database helper functions for inserting and retrieving session data. - Ensure schema changes are isolated and do not affect any existing databases or data. 4. RAG Pipeline Implementation - Implement the backend logic for: • Text chunking of book content • Generating embeddings using OpenAI or Claude Code embeddings • Vector search in Qdrant • Assembling assistant responses for the chatbot - All code should reside in `backend/` and not interfere with frontend mock responses. 5. Configuration & Environment Safety - Store all API keys, database URLs, and secrets in `.env` files. - Ensure no hard-coded credentials or changes to frontend configurations. - **The backend implementation must not overwrite any existing project data.** 6. Testing & Validation - Implement unit tests for each endpoint: • `/embed` — validate embeddings are stored correctly • `/query` — validate correct retrieval of text chunks • • `/chat` — validate response assembly - Simulate queries with dummy book content to ensure backend works independently. Deliverables: - Fully functional FastAPI backend with isolated folder structure. - Integration with Qdrant for embeddings and search. - Integration with Neon PostgreSQL for session management. - RAG pipeline ready for frontend integration. - All code additive, non-destructive to existing project files or git history. Non-Goals: - Do not connect to or modify existing frontend components. - Do not delete or overwrite previous mock frontend responses or project data. - Do not implement frontend rendering in this feature. End of specification."
labels: ["specification", "backend", "api", "rag", "fastapi", "qdrant", "neon"]
links:
  spec: specs/001-rag-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-backend-api/spec.md
  - specs/001-rag-backend-api/checklists/requirements.md
tests: []
---

## Prompt

```
Feature: 2.3 — Backend API Layer (FastAPI + Qdrant + Neon) Objective: Develop the backend services for the RAG chatbot, including book content embedding, vector search, chat session handling, and database integration. All implementation must be **isolated and additive**, ensuring no existing frontend components, project files, or git branches are deleted or modified. Requirements: 1. FastAPI Server Setup - Create a new FastAPI project under a separate folder, e.g., `backend/`. - Implement the following API endpoints: • `/embed` — Accept book content chunks and store embeddings in Qdrant. • `/query` — Accept user questions and return relevant text chunks from Qdrant. • `/chat` — Accept user input, retrieve relevant context, and return assistant response. - Enable CORS for frontend Docusaurus integration. - **Do not modify any existing frontend components or files.** 2. Qdrant Vector Database Integration - Set up a Qdrant collection specifically for book embeddings. - Implement functions to: • `upsert` embeddings • `search` nearest neighbors for a query - Store connection credentials in a `.env` file. - **Ensure all work is isolated and additive, without touching previous project files.** 3. Neon Serverless PostgreSQL Integration - Create database tables for: • User sessions • Optional chat history for analytics - Implement database helper functions for inserting and retrieving session data. - Ensure schema changes are isolated and do not affect any existing databases or data. 4. RAG Pipeline Implementation - Implement the backend logic for: • Text chunking of book content • Generating embeddings using OpenAI or Claude Code embeddings • Vector search in Qdrant • Assembling assistant responses for the chatbot - All code should reside in `backend/` and not interfere with frontend mock responses. 5. Configuration & Environment Safety - Store all API keys, database URLs, and secrets in `.env` files. - Ensure no hard-coded credentials or changes to frontend configurations. - **The backend implementation must not overwrite any existing project data.** 6. Testing & Validation - Implement unit tests for each endpoint: • `/embed` — validate embeddings are stored correctly • `/query` — validate correct retrieval of text chunks • • `/chat` — validate response assembly - Simulate queries with dummy book content to ensure backend works independently. Deliverables: - Fully functional FastAPI backend with isolated folder structure. - Integration with Qdrant for embeddings and search. - Integration with Neon PostgreSQL for session management. - RAG pipeline ready for frontend integration. - All code additive, non-destructive to existing project files or git history. Non-Goals: - Do not connect to or modify existing frontend components. - Do not delete or overwrite previous mock frontend responses or project data. - Do not implement frontend rendering in this feature. End of specification.
```

## Response snapshot

```
I have created the feature specification for the Backend API Layer (FastAPI + Qdrant + Neon). The specification includes detailed user scenarios, functional requirements, key entities, and measurable success criteria. I also created a corresponding quality checklist and performed a contextual validation, marking all items as passed with appropriate justifications given the explicit technology mentions in the user's prompt. The feature is ready for the /sp.plan phase.
```

## Outcome

- ✅ Impact: Successfully created the feature specification for the RAG chatbot backend API layer.
- 🧪 Tests: No automated tests were run during spec creation.
- 📁 Files: Created specs/001-rag-backend-api/spec.md and specs/001-rag-backend-api/checklists/requirements.md.
- 🔁 Next prompts: The spec is ready for the /sp.plan phase.
- 🧠 Reflection: Encountered difficulties with PowerShell script argument parsing due to the length and complexity of the feature description, necessitating manual file creation and population. Contextual interpretation was applied to checklist validation regarding technology mentions.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script execution failure due to argument parsing issues.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Improve the robustness of script argument parsing or provide clearer instructions for handling long feature descriptions.
