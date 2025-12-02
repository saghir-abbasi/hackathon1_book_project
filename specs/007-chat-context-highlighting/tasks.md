# Tasks for Feature 2.5: Chat Search, Highlighting & Context Injection UI

**Feature Branch**: `007-chat-context-highlighting`  
**Date**: 2025-12-02
**Spec**: `specs/007-chat-context-highlighting/spec.md`
**Plan**: `specs/007-chat-context-highlighting/plan.md`

## Summary

This document outlines the actionable, dependency-ordered tasks for implementing the "Chat Search, Highlighting & Context Injection UI" feature. Tasks are organized into phases corresponding to the feature's implementation stages and user stories.

## Dependency Graph (User Story Completion Order)

US1 (Highlight text and ask a question) --> US2 (Manage selected context)

## Parallel Execution Opportunities

- Frontend UI component development (e.g., `AskAboutThis.jsx`, `ContextBubble.jsx`) can largely be done in parallel with backend data model and API extensions, as long as the contract is agreed upon.
- Frontend hook development (`useTextSelection.js`) can be done in parallel with UI components.
- Sanitization logic can be developed for frontend and backend in parallel.

## Implementation Strategy

The implementation will follow an MVP-first approach, prioritizing User Story 1 to deliver core value quickly. Subsequent stories will be built incrementally.

---

## Phase 1: Setup

- [X] T001 Install `DOMPurify` in `docusaurus-book-site/package.json` (Frontend)
- [X] T002 Install `Bleach` and `html5lib` in `backend/requirements.txt` (Backend)
- [X] T003 Extend `ChatRequest` Pydantic model in `backend/src/models/chat_models.py` to include `selected_text: Optional[str]`, `chapter_id: Optional[str]`, `section_id: Optional[str]`, and `offsets: Optional[List[int]]`.

---

## Phase 2: User Story 1 - Highlight text and ask a question (Priority: P1)

**Goal**: As a user reading the book, I want to be able to select a passage of text and click an "Ask About This" button, so that I can get a specific answer from the chatbot based on that context.

**Independent Test**: Can be fully tested by selecting text, clicking the button, and asking a question. The value is delivered if the chatbot provides a contextual answer.

### Frontend: Text Selection Detection Layer

- [X] T004 [P] [US1] Create `useTextSelection.js` hook in `docusaurus-book-site/src/ai/hooks/useTextSelection.js`
- [X] T005 [P] [US1] Implement DOM event listeners (`mouseup`, `keyup`) in `useTextSelection.js` for text selection
- [X] T006 [P] [US1] Implement logic in `useTextSelection.js` to extract selected text, chapter ID, section ID, and character offsets
- [X] T007 [P] [US1] Implement client-side sanitization of `selectedText` using `DOMPurify` in `useTextSelection.js`
- [X] T008 [P] [US1] Implement maximum length enforcement (1000 characters) for `selectedText` in `useTextSelection.js`
- [X] T009 [US1] Integrate `useTextSelection` hook by modifying `docusaurus-book-site/src/theme/Layout/index.js` (swizzling)

### Frontend: UI Highlighting & Floating Action Button

- [X] T010 [P] [US1] Create CSS module for robotics-themed highlight (neon blue, grid pattern, rounded corners) in `docusaurus-book-site/src/css/custom.css` (or new dedicated CSS file)
- [X] T011 [P] [US1] Create `AskAboutThis.jsx` component in `docusaurus-book-site/src/ai/components/AskAboutThis.jsx`
- [X] T012 [P] [US1] Implement logic for `AskAboutThis.jsx` to appear near selection, using collected metadata
- [X] T013 [P] [US1] Implement mobile-friendly repositioning for `AskAboutThis.jsx`
- [X] T014 [P] [US1] Implement click handler for "Ask About This" button in `AskAboutThis.jsx` to send data to chatbot and open panel
- [X] T015 [P] [US1] Implement accessibility for keyboard navigation and screen readers for `AskAboutThis.jsx`

### Frontend: Frontend → Backend Metadata Pipeline Extension

- [X] T016 [US1] Modify `docusaurus-book-site/src/agent-client/chatClient.js` to accept `sectionId` and `offsets` in `sendMessage` and include in payload
- [X] T017 [US1] Modify `docusaurus-book-site/src/agent-client/agentBridge.js` to accept `sectionId` and `offsets` in `sendChatMessage` and pass to `chatClient.sendMessage`
- [X] T018 [US1] Integrate the call to `agentBridge.sendChatMessage` in the UI component (`AskAboutThis.jsx` or its parent) with the collected metadata from `useTextSelection`

### Backend: Metadata Processing

- [X] T019 [P] [US1] Create `metadata_injector.py` utility in `backend/src/utils/metadata_injector.py`
- [X] T020 [P] [US1] Implement `metadata_injector.py` to validate incoming metadata, strip HTML using `Bleach`, and enforce maximum length (1000 characters) for `selected_text`
- [X] T021 [US1] Integrate `metadata_injector.py` into the request processing flow in `backend/src/api/chat_router.py` to process incoming contextual metadata

### Backend: Agent Context Prioritization

- [X] T022 [US1] Modify `backend/src/api/chat_router.py` to extract `selected_text`, `chapter_id`, `section_id`, `offsets` from `ChatRequest` and pass to RAG service
- [X] T023 [US1] Modify `backend/src/services/rag_service.py` (`retrieve_relevant_segments`) to use `chapter_id` and `section_id` for Qdrant filtering
- [X] T024 [US1] Modify `backend/src/services/rag_service.py` (`generate_rag_response`) to incorporate `selected_text` into query embedding and LLM prompt with higher priority

---

## Phase 3: User Story 2 - Manage selected context (Priority: P2)

**Goal**: As a user, I want to be able to see and remove the context I've selected in the chatbot, so I can ask a general question without the context influencing the answer.

**Independent Test**: Can be tested by selecting text, opening the chatbot, and removing the context.

### Frontend: Context Bubble Integration in Chat Panel

- [X] T025 [P] [US2] Create `ContextBubble.jsx` component in `docusaurus-book-site/src/ai/components/ContextBubble.jsx`
- [X] T026 [P] [US2] Implement `ContextBubble.jsx` to display selected text, expand/collapse functionality, and a remove context button
- [X] T027 [US2] Create `contextIntegration.js` in `docusaurus-book-site/src/ai/chat/contextIntegration.js` for additive integration of `ContextBubble.jsx` into the chatbot UI
- [X] T028 [US2] Implement logic for removing context (clearing `selectedText` and other metadata in the frontend state) in `contextIntegration.js`

---

## Phase 4: Polish & Cross-Cutting Concerns

- [X] T029 Update `quickstart.md` in `specs/007-chat-context-highlighting/quickstart.md` with any new setup/testing details.
- [X] T030 Add unit and integration tests for new frontend components, hooks, and backend utilities.
- [X] T031 Ensure all new code adheres to documentation standards (docstrings, comments).
- [X] T032 Conduct end-to-end testing of the feature, covering all acceptance scenarios and edge cases identified in the spec.
