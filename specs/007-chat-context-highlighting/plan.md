# Implementation Plan: Chat Search, Highlighting & Context Injection UI

**Branch**: `007-chat-context-highlighting` | **Date**: 2025-12-02 | **Spec**: `specs/007-chat-context-highlighting/spec.md`
**Input**: Feature specification from `specs/007-chat-context-highlighting/spec.md`

## Summary

This plan outlines the step-by-step blueprint for implementing the Chat Search, Highlighting & Context Injection UI feature (Feature 2.5). This feature enables users to select text within the Docusaurus book, highlight it, and use an "Ask About This" button to send the selected content as context to the chatbot. The selected text will be displayed in a context bubble within the chat panel, influencing the agent's responses. The implementation will be strictly additive, ensuring no modification or deletion of existing project files, folders, branches, configs, or code.

## Technical Context

**Language/Version**:
- Frontend: TypeScript (React, Node.js 18+)
- Backend: Python 3.9+

**Primary Dependencies**:
- Frontend: React, Docusaurus
- Backend: FastAPI, Qdrant (vector DB), Gemini API / OpenAI API (LLM SDK)

**Storage**: Qdrant (Vector Database)

**Testing**:
- Frontend: Jest, React Testing Library (assumed)
- Backend: Pytest (assumed)

**Target Platform**:
- Frontend: Web (Browser)
- Backend: Linux server (Dockerized)

**Project Type**: Web application (Docusaurus frontend, Python FastAPI backend)

**Performance Goals**:
- Users can successfully ask a question about a selected passage of text and receive an answer derived from that text within 5 seconds.
- 100% of text selections trigger the "Ask About This" button.
- The contextual query success rate (agent uses the context correctly) is above 95%.

**Constraints**:
- Fully additive: No deletion, modification, or overwriting of existing project files, folders, branches, configs, or code.
- Existing chatbot UI, backend API, and agent logic must remain untouched except through additive integrations (e.g., new props, new modules, new extension hooks).
- Maximum selected text length: 1000 characters.

**Scale/Scope**: Typical web application scaling; focused on single-user interaction with the chatbot in a contextual manner.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [X] **Article I — Library-First & Modular Design**: All new components and utilities will be designed as separate, reusable modules.
- [X] **Article II — Spec-Driven & Test-First Workflow**: This planning phase follows the spec (Feature 2.5). Testing will be addressed in the `/sp.tasks` phase.
- [X] **Article III — Documentation, Content & Code Quality Standards**: New code will adhere to documentation standards.
- [X] **Article IV — Content & Deployment Standard (Book + UI)**: New frontend components integrate with Docusaurus.
- [X] **Article V — RAG & AI Integrations: Privacy, Security & Data Handling**: Selected text will be sanitized and length-limited, adhering to security best practices.
- [X] **Article VIII — Simplicity & Minimalism**: The additive nature of the feature prevents over-engineering or modification of existing systems.

## Project Structure

### Documentation (this feature)

```text
specs/007-chat-context-highlighting/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── services/
└── tests/

docusaurus-book-site/
├── src/
│   ├── agent-client/ (existing)
│   ├── components/ (existing)
│   ├── css/ (existing)
│   ├── pages/ (existing)
│   └── theme/ (existing)
└── tests/
```

**Structure Decision**: The project will follow a web application structure with additive components in both frontend and backend. New frontend modules will be created under `docusaurus-book-site/src/ai/` and new backend utilities under `backend/src/utils/`.

## Phase 0: Outline & Research

### Research Tasks

1.  **Task**: Investigate Docusaurus client-side DOM manipulation and event listening for text selection across pages.
    *   **Context**: How to reliably detect text selection, get selected text, and extract page/chapter/section metadata within a Docusaurus application environment.
    *   **Expected Outcome**: Understanding of Docusaurus DOM structure, React lifecycle hooks for event listeners, and methods to extract required metadata.

2.  **Task**: Identify the optimal integration points for new UI components within the existing Docusaurus setup (e.g., floating action button, chat panel context bubble).
    *   **Context**: Docusaurus uses React, so understanding how to add new React components additively without modifying core Docusaurus files is crucial.
    *   **Expected Outcome**: Strategy for component injection (e.g., using swizzling, custom plugins, or context providers).

3.  **Task**: Research best practices for sanitizing user-selected HTML content to prevent XSS and other injection attacks.
    *   **Context**: The selected text might contain malicious HTML or scripts.
    *   **Expected Outcome**: Identification of suitable libraries or methods for HTML stripping and content sanitization in both frontend (JS/TS) and backend (Python).

4.  **Task**: Understand the existing chat request builder and streaming pipeline in the frontend to determine the additive approach for metadata inclusion.
    *   **Context**: The feature must integrate selected context into existing streaming flow via additive parameters.
    *   **Expected Outcome**: Clear understanding of how to extend the request builder to include new metadata fields (`selectedText`, `chapterId`, `sectionId`, `offsets`) without breaking existing functionality.

5.  **Task**: Understand the existing agent request payload structure and how to inject the `selectedText` as a higher-priority context for RAG retrieval.
    *   **Context**: The agent should use `selectedText` as higher-priority context than regular RAG.
    *   **Expected Outcome**: Identification of the appropriate mechanism to modify the agent's prompt or context injection logic additively.

## Phase 1: Design & Contracts

### 1. Data Model (`specs/007-chat-context-highlighting/data-model.md`)

Will define the `SelectedContext` entity with its attributes (`selectedText`, `chapterId`, `sectionId`, `offsets`) and their types.

### 2. API Contracts (`specs/007-chat-context-highlighting/contracts/`)

Will define the extension to the existing chat API endpoint to accept the `SelectedContext` metadata. This will likely involve updating an existing request body schema or creating a new one if the current one is immutable.

### 3. Quickstart Guide (`specs/007-chat-context-highlighting/quickstart.md`)

Will provide a high-level guide on how to set up and test the new feature.

## Phase 2: Implementation (Tasks) - (To be generated by /sp.tasks)

The tasks will be broken down according to the phases described in the initial user prompt.

## Complexity Tracking

No violations of the Constitution have been identified for the planning phase.