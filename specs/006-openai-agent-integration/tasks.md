# Feature Tasks: Feature 2.4 — OpenAI Agents / ChatKit Integration

**Feature Branch**: `006-openai-agent-integration` | **Date**: December 2, 2025 | **Spec**: [specs/spec.md](spec.md)

## Phase 1: Setup

- [ ] T001 Create backend agent directory at `backend/app/agent/`.
- [ ] T002 Create subdirectories `tools/`, `system_prompts/`, and `runtime/` inside `backend/app/agent/`.
- [ ] T003 [P] Create `__init__.py` files in `backend/app/agent/`, `backend/app/agent/tools/`, and `backend/app/agent/runtime/`.
- [ ] T004 [P] Create frontend agent client directory at `docusaurus-book-site/src/agent-client/`.

## Phase 2: Foundational Tasks

- [ ] T005 Create and write the initial robotics-focused system prompt in `backend/app/agent/system_prompts/primary.txt`.
- [ ] T006 Implement the agent definition, configuration, and system prompt loader in `backend/app/agent/agent_definition.py`.
- [ ] T007 Implement helper functions for metadata packet preparation in `backend/app/agent/runtime/metadata.py`.
- [ ] T008 Implement rate limiting and input validation middleware in `backend/app/agent/security.py`.
- [ ] T009 Implement the OpenAI/ChatKit client wrapper with streaming and retry logic in `backend/app/agent/runtime/openai_client.py`.
- [ ] T010 Implement the core agent service to orchestrate agent, tools, and RAG calls in `backend/app/agent/services/agent_service.py`.

## Phase 3: User Story 1 - Ask a Question to the AI Assistant

**Goal**: As a user, I want to ask questions about the book's content through a chat interface so that I can quickly get relevant information.

**Independent Test**: This can be fully tested by interacting with the chat interface, submitting a question, and verifying that a streamed, contextually relevant response is received.

- [ ] T011 [US1] Implement the RAG tool for Qdrant vector search in `backend/app/agent/tools/rag_tool.py`.
- [ ] T012 [US1] Implement the selected text tool to validate and return selected text in `backend/app/agent/tools/selected_text_tool.py`.
- [ ] T013 [US1] Implement the chapter metadata tool in `backend/app/agent/tools/chapter_metadata_tool.py`.
- [ ] T014 [US1] Implement tool registration and binding in `backend/app/agent/runtime/tool_bindings.py`.
- [ ] T015 [US1] Implement the RAG binding function for vector search, scoring, and formatting in `backend/app/agent/runtime/rag_binding.py`.
- [ ] T016 [US1] Implement the `/agent/stream` endpoint in `backend/app/agent/router.py`.
- [ ] T017 [US1] [P] Implement the frontend chat client with `openStream()`, `sendMessage()`, and metadata injection in `docusaurus-book-site/src/agent-client/chatClient.js`.
- [ ] T018 [US1] [P] Implement the token-by-token event parser and rendering callbacks in `docusaurus-book-site/src/agent-client/streamHandler.js`.
- [ ] T019 [US1] Implement the UX integration layer to wrap the chat client and stream handler in `docusaurus-book-site/src/agent-client/agentBridge.js`.
- [ ] T020 [US1] [P] Create unit tests for the agent definition in `backend/tests/unit/test_agent_definition.py`.
- [ ] T021 [US1] [P] Create unit tests for the agent tools in `backend/tests/unit/test_agent_tools.py`.
- [ ] T022 [US1] Create integration tests for the agent, including tool usage and streaming, in `backend/tests/integration/test_agent_integration.py`.

## Phase 4: User Story 2 - AI Assistant Handles Disconnected Stream

**Goal**: As a user, I want the chat experience to be resilient to network interruptions so that my conversation is not lost and I can continue interacting with the AI assistant.

**Independent Test**: This can be tested by simulating network disconnections during an active streaming response and observing the system's ability to recover or inform the user.

- [ ] T023 [US2] Implement reconnect logic in `docusaurus-book-site/src/agent-client/chatClient.js`.
- [ ] T024 [US2] Implement disconnection handling and user notifications in `docusaurus-book-site/src/agent-client/streamHandler.js`.

## Phase 5: User Story 3 - AI Assistant Uses Configured Tools

**Goal**: As a user, I want the AI assistant to leverage its internal tools, such as the RAG system, to provide comprehensive and accurate answers from the book's content.

**Independent Test**: This can be tested by posing questions that specifically require the RAG tool to retrieve information that is not part of the agent's base knowledge but is present in the book content.

- [ ] T025 [US3] Enhance the agent service in `backend/app/agent/services/agent_service.py` to correctly use the RAG, selected text, and chapter metadata tools based on input.
- [ ] T026 [US3] Add or enhance unit tests in `backend/tests/unit/test_agent_tools.py` to verify correct tool usage and data flow.

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T027 Add comprehensive logging to the backend agent service in `backend/app/agent/services/agent_service.py`.
- [ ] T028 Review and refine abuse prevention mechanisms in `backend/app/agent/security.py`.
- [ ] T029 Update `quickstart.md` with final setup instructions and troubleshooting tips.

## Dependencies

- **User Story 1** must be completed before **User Story 2** and **User Story 3**.
- **User Story 2** and **User Story 3** can be implemented in parallel after **User Story 1** is complete.
- **Phase 6** should be completed after all user stories are implemented.

## Parallel Execution

- Within User Story 1, frontend tasks (T017, T018) can be developed in parallel with backend tasks (T011-T016).
- Unit tests (T020, T021) can be developed in parallel with their corresponding implementation tasks.

## Implementation Strategy

The implementation will follow a phased approach, starting with the setup and foundational backend components. The MVP (Minimum Viable Product) will be the completion of **User Story 1**, which delivers the core functionality of the AI assistant. Subsequent user stories will add robustness and enhanced capabilities. This approach ensures an incremental delivery of value and allows for early testing of the core feature.
