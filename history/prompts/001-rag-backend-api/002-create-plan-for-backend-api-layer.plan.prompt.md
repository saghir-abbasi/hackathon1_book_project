--- id: 002
title: Create Plan for Backend API Layer
stage: plan
date: 2025-12-01
surface: agent
model: gemini-pro
feature: 001-rag-backend-api
branch: 001-rag-backend-api
user: User
command: /sp.plan
labels: ["planning", "backend", "api", "rag", "fastapi", "qdrant", "neon"]
links:
  spec: specs/001-rag-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-backend-api/plan.md
  - specs/001-rag-backend-api/research.md
  - specs/001-rag-backend-api/data-model.md
  - specs/001-rag-backend-api/contracts/openapi.yaml
  - specs/001-rag-backend-api/quickstart.md
  - GEMINI.md
tests: []
---

## Prompt

```
---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.plan

Feature: 2.3 — Backend API Layer (FastAPI + Qdrant + Neon)

Goal:
Plan the development of a fully functional backend for the RAG chatbot that handles book content embedding, vector search, chat session management, and response assembly. The backend must be implemented in an **isolated, additive manner**, without altering existing frontend code or previous project data.

Plan:

1. Project Setup
   - Create a new folder `backend/` separate from the existing Docusaurus project.
   - Initialize a virtual environment and install dependencies:
     • FastAPI
     • Uvicorn
     • Qdrant client
     • Psycopg2 / SQLAlchemy for Neon PostgreSQL
     • dotenv for environment variables
   - Ensure **no existing files or git branches are touched**.

2. FastAPI Endpoint Planning
   - `/embed` — Accept book text chunks, generate embeddings, store in Qdrant.
   - `/query` — Accept user questions, retrieve relevant text chunks via vector search.
   - `/chat` — Combine query results to generate assistant response.
   - Include proper input validation and error handling.
   - Enable CORS for frontend integration.

3. Vector Database (Qdrant) Integration Plan
   - Define a dedicated collection for book embeddings.
   - Plan upsert, search, and delete (if needed) operations.
   - Secure connection using `.env` configuration.
   - Keep the integration fully isolated from other project data.

4. Neon Serverless PostgreSQL Plan
   - Plan database schema for:
     • User sessions
     • Optional chat history
   - Define tables, fields, and relations.
   - Ensure **additive-only creation**, no modification of existing databases.

5. Embedding & RAG Pipeline Plan
   - Chunk book text into smaller segments.
   - Generate embeddings using OpenAI or Claude Code embeddings.
   - Perform vector search in Qdrant.
   - Assemble retrieved text for assistant response.
   - Ensure backend logic is **isolated** from frontend components.

6. Environment & Security Plan
   - Store API keys, DB credentials, and secrets in `.env`.
   - Ensure no hard-coded keys or paths.
   - Verify the backend folder is self-contained.

7. Testing & Validation Plan
   - Unit tests for `/embed`, `/query`, `/chat`.
   - Use dummy book content to simulate retrieval and responses.
   - Verify endpoints work independently of frontend.
   - Ensure no previous project files or git history are altered.

8. Completion Criteria
   - Backend endpoints operational and tested.
   - Vector search and embeddings functional.
   - PostgreSQL integration implemented.
   - Backend code additive, isolated, and ready for frontend integration in Feature 2.4.

End of plan.
```

## Response snapshot

```
I have executed the planning workflow and generated the following design artifacts:
- plan.md: Outlines the detailed implementation strategy, technical context, and constitutional compliance.
- research.md: Documents the technology choices and rationale.
- data-model.md: Defines the data structures for the backend, including Qdrant and PostgreSQL entities.
- contracts/openapi.yaml: Provides the OpenAPI specification for the API endpoints (/embed, /query, /chat).
- quickstart.md: Offers instructions for setting up and running the backend locally.
- GEMINI.md: Updated with new technology context.

The feature is ready for the /sp.tasks phase.
```

## Outcome

- ✅ Impact: Successfully completed the planning phase for the Backend API Layer, generating all required design artifacts.
- 🧪 Tests: No automated tests were run during the planning phase.
- 📁 Files: Generated specs/001-rag-backend-api/plan.md, specs/001-rag-backend-api/research.md, specs/001-rag-backend-api/data-model.md, specs/001-rag-backend-api/contracts/openapi.yaml, specs/001-rag-backend-api/quickstart.md, and updated GEMINI.md.
- 🔁 Next prompts: The plan is ready for the /sp.tasks phase.
- 🧠 Reflection: Successfully generated all planning artifacts, including a detailed plan, research document, data model, API contracts, and quickstart guide. The agent context was also updated to include the new backend technologies.

## Evaluation notes (flywheel)

- Failure modes observed: Bash script execution failure in PowerShell environment (addressed by manual PHR creation).
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Improve the robustness of the PHR creation process to be less dependent on shell script execution in cross-platform environments.
