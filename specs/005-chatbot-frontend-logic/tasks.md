# Tasks: Chatbot Frontend Logic & UX Enhancements

**Input**: Design documents from `/specs/005-chatbot-frontend-logic/`
**Prerequisites**: plan.md (required), spec.md (user stories derived from prompt), research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic dependencies

- [ ] T001 Install new dependencies (`zustand`, `react-markdown`, `remark-gfm`, `react-syntax-highlighter`) in `docusaurus-book-site/package.json`.
- [ ] T002 Refactor `docusaurus-book-site/src/components/chatbot/index.tsx` content to `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.
- [ ] T003 Update `docusaurus-book-site/src/components/chatbot/index.tsx` to re-export `ChatContainer`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create `docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts` with `Message` and `ChatState` types and `ChatActions` per `data-model.md`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - State Management Setup 🎯 MVP

**Goal**: Establish the core client-side state management for the chatbot.

**Independent Test**: Verify `useChatStore` initializes correctly and actions can modify state.

### Implementation for User Story 1

- [ ] T005 [P] [US1] Implement `addMessage(message: Message)` action in `docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts`.
- [ ] T006 [P] [US1] Implement `setLoading(isLoading: boolean)` action in `docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts`.
- [ ] T007 [P] [US1] Implement `setContextMode(mode: 'full_book' | 'selected_text')` action in `docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts`.
- [ ] T008 [P] [US1] Implement `resetChat()` action in `docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts`.

---

## Phase 4: User Story 2 - ChatContainer Integration

**Goal**: Orchestrate chat logic, state hooks, and manage message sending/auto-scroll.

**Independent Test**: Verify `ChatContainer` displays messages, sends mock responses, and auto-scrolls.

### Implementation for User Story 2

- [ ] T009 [US2] Integrate `useChatStore` into `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.
- [ ] T010 [US2] Implement orchestrator logic for sending messages in `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.
- [ ] T011 [US2] Implement auto-scroll on new message in `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.
- [ ] T012 [US2] Update `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx` to render `MessageList` (to be created in US3).

---

## Phase 5: User Story 3 - MessageList Component

**Goal**: Display an ordered list of messages with auto-scroll and animation.

**Independent Test**: Verify `MessageList` renders messages and auto-scrolls to the bottom.

### Implementation for User Story 3

- [ ] T013 [US3] Create `docusaurus-book-site/src/components/chatbot/MessageList.tsx` to render ordered list of messages.
- [ ] T014 [US3] Implement auto-scroll-to-bottom behavior in `docusaurus-book-site/src/components/chatbot/MessageList.tsx`.
- [ ] T015 [US3] Add fade-in animation for new messages in `docusaurus-book-site/src/components/chatbot/MessageList.tsx`.

---

## Phase 6: User Story 4 - MessageBubble Component

**Goal**: Display individual messages with distinct styles and Markdown rendering.

**Independent Test**: Verify `MessageBubble` renders user/assistant messages with Markdown and syntax highlighting.

### Implementation for User Story 4

- [ ] T016 [US4] Create `docusaurus-book-site/src/components/chatbot/MessageBubble.tsx` to display user vs assistant messages.
- [ ] T017 [US4] Apply robotics-themed color palette for distinct styles in `docusaurus-book-site/src/components/chatbot/MessageBubble.tsx` and `docusaurus-book-site/src/css/custom.css`.
- [ ] T018 [US4] Support Markdown rendering using `react-markdown` + `remark-gfm` in `docusaurus-book-site/src/components/chatbot/MessageBubble.tsx`.
- [ ] T019 [US4] Add syntax highlighting for code blocks using `react-syntax-highlighter` in `docusaurus-book-site/src/components/chatbot/MessageBubble.tsx`.

---

## Phase 7: User Story 5 - ChatInput Component

**Goal**: Provide a multi-line input field with send functionality and disabled states.

**Independent Test**: Verify `ChatInput` handles multi-line input, send via Enter, and disables when loading.

### Implementation for User Story 5

- [ ] T020 [US5] Refactor `docusaurus-book-site/src/components/chatbot/ChatInput.tsx` to be a multi-line input field.
- [ ] T021 [US5] Implement `Enter` to send message and `Shift+Enter` for newline in `docusaurus-book-site/src/components/chatbot/ChatInput.tsx`.
- [ ] T022 [US5] Disable input while assistant is responding using `isLoading` state in `docusaurus-book-site/src/components/chatbot/ChatInput.tsx`.
- [ ] T023 [US5] Handle empty message prevention in `docusaurus-book-site/src/components/chatbot/ChatInput.tsx`.

---

## Phase 8: User Story 6 - LoadingIndicator Component

**Goal**: Provide visual feedback when the assistant is responding.

**Independent Test**: Verify `LoadingIndicator` displays during loading state.

### Implementation for User Story 6

- [ ] T024 [US6] Create `docusaurus-book-site/src/components/chatbot/LoadingIndicator.tsx` for animated assistant “typing…” indicator.
- [ ] T025 [US6] Display `LoadingIndicator` during `isLoading` state in `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.

---

## Phase 9: User Story 7 - ContextModeSelector Component

**Goal**: Allow users to select the context for the chatbot.

**Independent Test**: Verify `ContextModeSelector` allows switching between modes and shows placeholder.

### Implementation for User Story 7

- [ ] T026 [US7] Create `docusaurus-book-site/src/components/chatbot/ContextModeSelector.tsx` for dropdown/toggle.
- [ ] T027 [US7] Implement context selection logic and integrate `setContextMode` from `useChatStore` in `docusaurus-book-site/src/components/chatbot/ContextModeSelector.tsx`.
- [ ] T028 [US7] Show placeholder UI box for selected text preview (frontend-only) in `docusaurus-book-site/src/components/chatbot/ContextModeSelector.tsx`.
- [ ] T029 [US7] Integrate `ContextModeSelector` into `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.

---

## Phase 10: User Story 8 - Mock Assistant Response Module

**Goal**: Simulate assistant responses for frontend development.

**Independent Test**: Verify mock assistant returns placeholder text with delay.

### Implementation for User Story 8

- [ ] T030 [US8] Create async function `simulateAssistantReply()` with random delay (500–900ms) and placeholder response.
- [ ] T031 [US8] Integrate `simulateAssistantReply()` with `ChatContainer` logic to trigger mock assistant responses and update `isLoading` state in `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.

---

## Phase 11: User Story 9 - Error & Reset Handling

**Goal**: Implement UI for error messages and chat reset functionality.

**Independent Test**: Verify error messages display and `resetChat` clears the conversation.

### Implementation for User Story 9

- [ ] T032 [US9] Implement UI logic for simulated message-send error using `error` state in `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.
- [ ] T033 [US9] Provide retry functionality for errors in `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.
- [ ] T034 [US9] Implement `resetChat()` button logic in `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx` using `resetChat` action.

---

## Phase 12: User Story 10 - Robotics-Themed Design Integration

**Goal**: Apply a consistent robotics theme across all chatbot components.

**Independent Test**: Verify consistent theme, responsiveness, and dark mode compatibility.

### Implementation for User Story 10

- [ ] T035 [US10] Apply consistent styling (deep blue, silver, neon cyan accents, clean geometric fonts) to chatbot components in `docusaurus-book-site/src/css/custom.css` and `docusaurus-book-site/src/components/chatbot/chatbot.module.css`.
- [ ] T036 [US10] Ensure dark mode compatibility for all chatbot UI elements.
- [ ] T037 [US10] Test responsiveness and layout spacing of chatbot UI.

---

## Phase 13: User Story 11 - Final Assembly & Testing

**Goal**: Integrate all components, validate functionality, and update documentation.

**Independent Test**: Verify end-to-end message flow, UX smoothness, and updated documentation.

### Implementation for User Story 11

- [ ] T038 [US11] Wire all chatbot components together within `docusaurus-book-site/src/components/chatbot/ChatContainer.tsx`.
- [ ] T039 [US11] Validate message flow, input behavior, auto-scroll, and context selector.
- [ ] T040 [US11] Verify theming, animations, and overall UX smoothness.
- [ ] T041 [US11] Update `docusaurus-book-site/src/components/chatbot/README.md` with new component hierarchy, Zustand usage, Markdown rendering, and context mode.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T042 Code cleanup and refactoring in `docusaurus-book-site/src/components/chatbot/`.
- [ ] T043 Run quickstart.md validation to ensure all features work as expected.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (State Management Setup)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 2 (ChatContainer Integration)**: Depends on US1 (for Zustand integration) and partially on US3 (MessageList).
- **User Story 3 (MessageList Component)**: Depends on US4 (MessageBubble).
- **User Story 4 (MessageBubble Component)**: Can start after Foundational (Phase 2).
- **User Story 5 (ChatInput Component)**: Depends on US1 (for `isLoading` state).
- **User Story 6 (LoadingIndicator Component)**: Depends on US1 (for `isLoading` state).
- **User Story 7 (ContextModeSelector Component)**: Depends on US1 (for `setContextMode` action).
- **User Story 8 (Mock Assistant Response Module)**: Depends on US1 (for `addMessage`, `setLoading`).
- **User Story 9 (Error & Reset Handling)**: Depends on US1 (for `setError`, `resetChat`).
- **User Story 10 (Robotics-Themed Design Integration)**: Can run in parallel with other component implementations, but final review after all components are built.
- **User Story 11 (Final Assembly & Testing)**: Depends on completion of US1-US10.

### Within Each User Story

- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- All tasks marked [P] can run in parallel.
- Once Foundational phase completes, several user stories can start in parallel (e.g., US1, US4, US5, US6, US7, US8, US9, US10 components can be scaffolded).
- Different user stories can be worked on in parallel by different team members, respecting dependencies.

---

## Parallel Example: User Story 1

```bash
# All tasks for User Story 1 can be developed in parallel:
Task: "Implement `addMessage(message: Message)` action in docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts"
Task: "Implement `setLoading(isLoading: boolean)` action in docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts"
Task: "Implement `setContextMode(mode: 'full_book' | 'selected_text')` action in docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts"
Task: "Implement `resetChat()` action in docusaurus-book-site/src/components/chatbot/hooks/useChatStore.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 & Foundational)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (State Management Setup)
4.  **STOP and VALIDATE**: Test User Story 1 functionality (store initialization, actions).
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently
3.  Add User Story 4 (MessageBubble) → Test independently
4.  Add User Story 3 (MessageList, depending on US4) → Test independently
5.  Add User Story 2 (ChatContainer, depending on US1, US3) → Test independently
6.  Proceed with other stories in a logical, dependent order (e.g., US5, US6, US7, US8, US9, US10).
7.  Finally, US11 for final assembly and testing.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Developer A: User Story 1 (State Management)
    *   Developer B: User Story 4 (MessageBubble Component)
    *   Developer C: User Story 5 (ChatInput Component)
    *   Developer D: User Story 6 (LoadingIndicator Component)
    *   Developer E: User Story 7 (ContextModeSelector Component)
    *   Developer F: User Story 8 (Mock Assistant)
    *   Developer G: User Story 9 (Error & Reset)
    *   Developer H: User Story 10 (Theming, can start early and refine)
3.  Stories with dependencies (US2, US3) can then be picked up as their prerequisites are completed.
4.  US11 (Final Assembly) will integrate all completed components.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable where possible.
-   Commit after each task or logical group.
-   Stop at any checkpoint to validate story independently.
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
