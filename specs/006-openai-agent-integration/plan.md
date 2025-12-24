# Implementation Plan: [FEATURE]

**Branch**: `006-openai-agent-integration` | **Date**: December 2, 2025 | **Spec**: specs/006-openai-agent-integration/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of an intelligent agent layer that integrates with the Docusaurus frontend and the FastAPI backend. The objective is to create a fully operational, streamed-response AI assistant capable of answering queries using the book’s knowledge via Retrieval Augmented Generation (RAG). The technical approach involves designing a new, isolated backend agent architecture, setting up a tools layer for RAG, selected text processing, and chapter metadata, defining a modular system prompt strategy, and exposing a new streaming API from the backend. On the frontend, a new client-side SDK will be integrated into the Docusaurus plugin folder to manage communication with the streaming backend, enabling a dynamic chat UX with loading states and token-by-token rendering. Robust security measures and abuse prevention mechanisms will be implemented, and a comprehensive testing and validation strategy will ensure a zero-impact, additive integration.

## Technical Context

**Language/Version**: Python 3.12, TypeScript
**Primary Dependencies**: FastAPI, React, OpenAI/ChatKit SDK, Qdrant
**Storage**: Qdrant (vector storage), Neon DB (chat/session storage)
**Testing**: pytest (backend), Jest with React Testing Library (frontend)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Streaming Response: P90 latency < 5 seconds; Concurrency: 50 concurrent users
**Constraints**: All implementation MUST be additive and MUST NOT modify or delete any existing project data, files, branches, history, or directories.
**Scale/Scope**: DAU: <100; Queries: <500

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Article I — Library-First & Modular Design**: PASS. The plan focuses on creating isolated and new components, aligning with modular design principles.
- **Article II — Spec-Driven & Test-First Workflow**: PASS. This plan is derived from a detailed specification and explicitly includes testing in later phases.
- **Article III — Documentation, Content & Code Quality Standards**: PASS. The plan includes the generation of documentation artifacts like `data-model.md`, API contracts, and a `quickstart.md`.
- **Article IV — Content & Deployment Standard (Book + UI)**: PASS. The plan respects the existing Docusaurus frontend and ensures dynamic behavior is isolated to the new AI assistant.
- **Article V — RAG & AI Integrations: Privacy, Security & Data Handling**: PASS. Dedicated sections for security measures (API key management, input sanitization) are included.
- **Article VI — Reusable Intelligence: Subagents & Agent Skills**: PASS. The design of the tools layer promotes reusability and modular skills for the AI assistant.
- **Article VII — Internationalization & Personalization Support**: N/A. This feature does not directly impact these aspects.
- **Article VIII — Simplicity & Minimalism**: PASS. The approach is additive, creating new, isolated components without over-engineering existing systems.
- **Article IX — Version Control, Release & Traceability**: PASS. The development is within a version-controlled environment, and the process supports traceability.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
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
│   │   └── agent_router.py # New API router for agent stream
│   ├── app/
│   │   └── agent/
│   │       ├── __init__.py
│   │       ├── agent_definition.py # Agent configuration and definition
│   │       ├── tools/
│   │       │   ├── __init__.py
│   │       │   ├── rag_tool.py # RAG tool implementation
│   │       │   ├── selected_text_tool.py # Selected text tool implementation
│   │       │   └── chapter_metadata_tool.py # Chapter metadata tool implementation
│   │       └── system_prompts/
│   │           └── primary.txt # Robotics-aligned system prompt
│   └── services/
│       └── agent_service.py # Orchestrates agent, tools, RAG calls
├── tests/
│   ├── integration/
│   │   └── test_agent_integration.py # New integration tests for agent
│   └── unit/
│       ├── test_agent_definition.py # New unit tests for agent definition
│       └── test_agent_tools.py # New unit tests for agent tools
└── .env # API keys
    
docusaurus-book-site/
├── plugins/
│   └── local-chat-plugin/ # Example plugin path
│       └── chatClient.js # New client-side SDK integration
└── src/
    └── components/
        └── ChatUIExtension.js # Extension for existing chat UI, no modification of original
```

**Structure Decision**: The project structure will primarily follow the existing `backend/` and `docusaurus-book-site/` conventions. All new components for the AI agent and its integration will be additive and housed within new directories and files to ensure zero impact on existing codebases. The `backend/app/agent/` directory will encapsulate the agent's core logic, tools, and system prompts. New API routing will be added under `backend/src/api/`, and services under `backend/src/services/`. Frontend integration will occur within a new Docusaurus plugin and an extension to the existing chat UI.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
