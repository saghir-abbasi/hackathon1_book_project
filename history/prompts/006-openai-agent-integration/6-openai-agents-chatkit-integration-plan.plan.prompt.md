---
id: 6
title: OpenAI Agents ChatKit Integration Plan
stage: plan
date: 2025-12-02
surface: agent
model: gemini-1.5-pro
feature: 006-openai-agent-integration
branch: 006-openai-agent-integration
user:
  id: default
  email: default@example.com
command: /sp.plan
labels:
  - plan
  - openai-agents
  - chatkit
  - rag
links:
  spec: specs/006-openai-agent-integration/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/006-openai-agent-integration/plan.md
  - specs/006-openai-agent-integration/research.md
  - specs/006-openai-agent-integration/data-model.md
  - specs/006-openai-agent-integration/contracts/openapi.yaml
  - specs/006-openai-agent-integration/quickstart.md
tests_yaml: []
prompt_text: |
  /sp.plan

  Create an implementation plan for Feature 2.4 — OpenAI Agents / ChatKit Integration.

  Follow these planning requirements:

  GENERAL SAFETY REQUIREMENTS:
  - DO NOT delete, modify, overwrite, or restructure any existing project data, files, branches, history, or directories.
  - All new work must be fully additive and placed inside new folders or new files.
  - The existing Docusaurus frontend, backend API (Feature 2.3), and book content must remain untouched.
  - Any integration must only extend functionality, never replace or alter existing modules.

  ---

  PLAN SCOPE:
  Design a step-by-step blueprint to integrate OpenAI Agents / ChatKit with the FastAPI backend and Docusaurus frontend, resulting in a fully functional RAG-enabled AI assistant with streamed responses.

  The plan must cover:

  1. **New Backend Agent Architecture**
     - Create an isolated folder `backend/app/agent/`.
     - Define agent configuration, system prompts, tool registration, and metadata injection.
     - Ensure the agent safely calls:
       • RAG retrieval
       • embeddings
       • Neon session store
     - No interference with existing backend code.

  2. **Tools Layer Setup**
     - Define individual Python modules for tools:
       • RAG tool (Qdrant search)
       • Selected-text tool
       • Chapter metadata tool
     - Bind tools to agent runtime.

  3. **System Prompt Strategy**
     - Add a dedicated `system_prompts/` folder.
     - Write robotics-aligned system prompt referencing book themes.
     - Ensure prompt is modular and easily extensible.

  4. **Backend Streaming API**
     - Add a new router `/agent/stream` using SSE or chunked streaming.
     - Wrap OpenAI/ChatKit streaming outputs.
     - Ensure no existing endpoints are modified.

  5. **Frontend ChatKit/OpenAI SDK Integration**
     - Add a NEW file `chatClient.js` or `chatBridge.js` under Docusaurus plugin folder.
     - Implement:
       • sendMessage()
       • openStream()
       • reconnect logic
     - Pass metadata: selected text, chapter ID, session ID.

  6. **Streaming UX Integration**
     - Extend existing chat UI by adding listeners to the streaming client.
     - Ensure no prior UI components are deleted or rewritten.
     - Add loading states, retry notifications, token-by-token rendering.

  7. **Security Measures**
     - Move all API keys to backend `.env` only.
     - Add middleware for:
       • rate limiting
       • prompt sanitization
       • metadata validation
     - Ensure frontend never receives sensitive data.

  8. **Abuse Prevention**
     - Implement server-side safeguards:
       • max prompt length
       • max selected-text size
       • output token caps
     - Add request throttling per session.

  9. **Frontend-Backend-Agent Bridge**
     - Design the full message flow:
       Docusaurus → chatClient → `/agent/stream` → Agent → Streamed tokens → UI.
     - Ensure streaming remains smooth and resilient.

  10. **Testing & Validation**
      - Add tests in backend:
        • agent boot test
        • RAG tool test
        • streaming test
        • metadata injection test
      - Add frontend test messages using mock text.

  11. **Zero-Impact Integration Assurance**
      - Validate that:
        • No existing backend routes change
        • No original project files are altered
        • No book data, UI, or Git history is affected
        • All changes remain strictly additive

  Produce the final plan with phases, sequencing, prerequisites, and dependencies while maintaining all safety restrictions.
response_text: |
  The implementation plan for "Feature 2.4 — OpenAI Agents / ChatKit Integration" has been successfully generated.
  Branch: `006-openai-agent-integration`
  Implementation Plan Path: `specs/006-openai-agent-integration/plan.md`
  Generated Artifacts:
  - `specs/006-openai-agent-integration/research.md`
  - `specs/006-openai-agent-integration/data-model.md`
  - `specs/006-openai-agent-integration/contracts/openapi.yaml`
  - `specs/006-openai-agent-integration/quickstart.md`

  The plan is ready for review and proceeding to the next phase (e.g., tasks).
outcome: ""
evaluation: ""
---