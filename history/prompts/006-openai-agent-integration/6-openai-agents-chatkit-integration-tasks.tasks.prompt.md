---
id: 6
title: OpenAI Agents ChatKit Integration Tasks
stage: tasks
date: 2025-12-02
surface: agent
model: gemini-1.5-pro
feature: 006-openai-agent-integration
branch: 006-openai-agent-integration
user:
  id: default
  email: default@example.com
command: /sp.tasks
labels:
  - tasks
  - openai-agents
  - chatkit
  - rag
links:
  spec: specs/006-openai-agent-integration/spec.md
  plan: specs/006-openai-agent-integration/plan.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/006-openai-agent-integration/tasks.md
tests_yaml: []
prompt_text: |
  /sp.tasks

  Generate a complete list of development tasks for Feature 2.4 — OpenAI Agents / ChatKit Integration.

  IMPORTANT SAFETY RULES (MUST APPLY TO ALL TASKS):
  - DO NOT delete, modify, or overwrite any previously created project files, data, folders, or git branches.
  - All new work must be additive only.
  - All new backend logic must be placed inside new, dedicated folders under `backend/app/agent/`.
  - All new frontend logic must be placed in new files inside a Docusaurus plugin or a new folder (e.g., `src/agent-client/`), without editing existing Docusaurus or chat UI files.

  ---

  TASKS BREAKDOWN:
  ### 1. Backend Agent Folder Setup
  - Create new directory: `backend/app/agent/`.
  - Create subfolders: `tools/`, `system_prompts/`, `runtime/`.
  - Add `__init__.py` files to each folder.

  ### 2. Agent Definition Module
  - Add `agent_definition.py` with:
    • agent name, description
    • model configuration
    • system prompt loader
    • tool registry interface
  - Ensure this file does not import or modify existing backend modules.

  ### 3. System Prompt Creation
  - Create file: `system_prompts/primary.txt`.
  - Write robotics-focused system prompt:
    • Physical AI
    • Humanoid Robotics
    • ROS 2 → Gazebo → Isaac → VLA
    • Book-grounded reasoning rules
  - Ensure no previous prompts are altered.

  ### 4. Tools Implementation
  - Add separate tool modules:
    • `tools/rag_tool.py` — calls Qdrant vector search
    • `tools/selected_text_tool.py` — validates and returns selected text
    • `tools/chapter_metadata_tool.py` — returns chapter metadata
  - Tools must:
    • Follow a consistent JSON return schema
    • Validate inputs
    • Never mutate external state
    • Interact with Feature 2.3 backend through imports without modifying it

  ### 5. Bind Tools to Agent
  - Create file `runtime/tool_bindings.py`.
  - Register all tools to the agent.
  - Ensure no existing runtime systems are modified.

  ### 6. RAG Binding Function
  - Add new file `runtime/rag_binding.py`.
  - Implement:
    • Vector search
    • Result scoring
    • Retrieval formatting
  - Use only Feature 2.3 APIs without modifying them.

  ### 7. Backend Streaming Endpoint
  - Add new router file: `backend/app/agent/router.py`.
  - Implement `/agent/stream` using SSE or chunked streaming.
  - Connect streaming output to OpenAI/ChatKit client inside backend.
  - Ensure existing FastAPI routes remain untouched.

  ### 8. Backend OpenAI/ChatKit Client
  - Add file: `runtime/openai_client.py`.
  - Implement:
    • streaming wrapper
    • retry logic
    • graceful error formatting
  - Load all secrets from `.env`.
  - Never expose keys to frontend.

  ### 9. Frontend ChatKit / OpenAI SDK Client
  - Create new folder: `src/agent-client/`.
  - Add `chatClient.js`:
    • openStream()
    • sendMessage()
    • reconnect logic
    • metadata injection (selected text, chapter ID, session ID)
  - Ensure no existing JS files are edited.

  ### 10. Streaming Handler in Frontend
  - Add `streamHandler.js`:
    • token-by-token event parsing
    • incremental rendering callbacks
    • disconnection handling

  ### 11. UX Integration Layer
  - Add file `agentBridge.js`:
    • wraps chatClient + streamHandler
    • exposes `sendChatMessage()` for chat UI
  - Ensure no changes to existing React components.

  ### 12. Security Tasks
  - Add backend rate limiting middleware inside a NEW file:
    • `backend/app/agent/security.py`
  - Implement:
    • prompt-length validation
    • selected-text size cap
    • token output cap
  - Ensure enforcement affects only the agent endpoints.

  ### 13. Metadata Injection Tasks
  - Add new helper file `runtime/metadata.py`.
  - Prepare metadata packet:
    • chapter ID
    • selected text
    • user session
    • timestamp
  - Inject metadata into agent requests.

  ### 14. Abuse Prevention Tasks
  - Add validation functions:
    • reject unusually large inputs
    • enforce safe ranges
  - Ensure rule
response_text: |
  The `tasks.md` file for "Feature 2.4 — OpenAI Agents / ChatKit Integration" has been successfully generated.
  Tasks File Path: `specs/006-openai-agent-integration/tasks.md`

  Summary:
  - Total Tasks: 29
  - Tasks per User Story:
    - User Story 1: 12 tasks
    - User Story 2: 2 tasks
    - User Story 3: 2 tasks
  - Parallel Opportunities: Identified within User Story 1 (frontend and backend development, unit testing) and between User Story 2 and 3.
  - Independent Test Criteria: Included for each user story.
  - Suggested MVP Scope: User Story 1 (Ask a Question to the AI Assistant).

  The tasks are now ready for implementation.
outcome: ""
evaluation: ""
---