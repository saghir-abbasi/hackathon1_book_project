# Tasks: Chatbot UI Shell in Docusaurus

**Input**: Design documents from `specs/004-chatbot-ui-shell/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md

## Format: `[ID] [P?] [Story] Description`

-   **[P]**: Can run in parallel (different files, no dependencies)
-   **[Story]**: Which user story this task belongs to (e.g., US1, US2)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the component file and directory structure.

- [x] T001 [P] Create directory `docusaurus-book-site/src/components/chatbot/`

- [x] T002 [P] Create directory `docusaurus-book-site/src/components/chatbot/components/`

- [x] T003 [P] Create empty file `docusaurus-book-site/src/components/chatbot/index.tsx`

- [x] T004 [P] Create empty file `docusaurus-book-site/src/components/chatbot/ChatbotButton.tsx`

- [x] T005 [P] Create empty file `docusaurus-book-site/src/components/chatbot/ChatWindow.tsx`

- [x] T006 [P] Create empty file `docusaurus-book-site/src/components/chatbot/components/ChatMessage.tsx`

- [x] T007 [P] Create empty file `docusaurus-book-site/src/components/chatbot/components/ChatInput.tsx`

- [x] T008 [P] Create empty file `docusaurus-book-site/src/components/chatbot/chatbot.module.css`

---

## Phase 2: User Story 1 - View and Open the Chatbot (Priority: P1) 🎯 MVP

**Goal**: A user can see a chatbot button on all pages and click it to open and close the chat window.

**Independent Test**: The floating chatbot button appears on every page. Clicking it toggles the visibility of the chat window panel.

### Implementation for User Story 1

- [x] T009 [US1] Implement the static JSX structure for the floating button in `docusaurus-book-site/src/components/chatbot/ChatbotButton.tsx`. It should accept an `onClick` prop.
- [x] T010 [US1] Implement the basic layout for the chat panel in `docusaurus-book-site/src/components/chatbot/ChatWindow.tsx`, including a header with the title "AI Assistant" and a close button.
- [x] T011 [US1] In the main container `docusaurus-book-site/src/components/chatbot/index.tsx`, import `ChatbotButton` and `ChatWindow`.
- [x] T012 [US1] In `docusaurus-book-site/src/components/chatbot/index.tsx`, add `useState` to manage the `isOpen` state of the chat window.
- [x] T013 [US1] In `docusaurus-book-site/src/components/chatbot/index.tsx`, render `ChatbotButton` and pass it a function to toggle the `isOpen` state.
- [x] T014 [US1] In `docusaurus-book-site/src/components/chatbot/index.tsx`, conditionally render `ChatWindow` based on the `isOpen` state.
- [x] T015 [US1] In `docusaurus-book-site/src/components/chatbot/chatbot.module.css`, add initial styles for the floating button's position, appearance, and hover effect.
- [x] T016 [US1] In `docusaurus-book-site/src/components/chatbot/chatbot.module.css`, add styles for the `ChatWindow` panel's position, size, header, and basic layout.
- [x] T017 [US1] In `docusaurus-book-site/src/components/chatbot/chatbot.module.css`, implement the CSS transitions for the smooth open/close animation of the chat window.
- [x] T018 [US1] Swizzle the Docusaurus `Root` component by running `npm run swizzle @docusaurus/theme-classic Root -- --danger` in the `docusaurus-book-site` directory. (SKIPPED by user request)
- [x] T019 [US1] In the newly created `docusaurus-book-site/src/theme/Root.tsx`, import and render the main `Chatbot` container to make it globally available.

**Checkpoint**: User Story 1 is functional. The chatbot button appears and toggles the chat window.

---

## Phase 3: User Story 2 - Interact with the Chatbot (Priority: P2)

**Goal**: A user can send a message in the chat window and receive a simulated, placeholder response.

**Independent Test**: Type a message, press Enter or click Send. The message appears in the chat history, followed by a "Thinking..." indicator and then a placeholder bot response.

### Implementation for User Story 2

- [x] T020 [P] [US2] Implement the static JSX for the message input form in `docusaurus-book-site/src/components/chatbot/components/ChatInput.tsx`.

- [x] T021 [P] [US2] Implement the static JSX for displaying a single message in `docusaurus-book-site/src/components/chatbot/components/ChatMessage.tsx`. It should accept message content and sender type as props.
- [x] T022 [US2] In `docusaurus-book-site/src/components/chatbot/index.tsx`, add state for `messages` (an array) and `isThinking` (a boolean) using `useState`, based on `data-model.md`.
- [x] T023 [US2] In `docusaurus-book-site/src/components/chatbot/index.tsx`, implement the `handleSendMessage` function. This function will add the user's message to the `messages` array and use a `setTimeout` to simulate a bot reply.
- [x] T024 [US2] In `docusaurus-book-site/src/components/chatbot/ChatWindow.tsx`, map over the `messages` state array and render a `ChatMessage` for each item.
- [x] T025 [US2] In `docusaurus-book-site/src/components/chatbot/ChatWindow.tsx`, pass the `handleSendMessage` function to the `ChatInput` component.
- [x] T026 [US2] In `docusaurus-book-site/src/components/chatbot/ChatWindow.tsx`, add a `div` to show the "Thinking..." indicator, conditionally rendered based on the `isThinking` state.
- [x] T027 [US2] Implement the auto-scroll behavior. In `ChatWindow.tsx`, use a `ref` on the message list container and a `useEffect` hook to scroll to the bottom when the `messages` array changes.
- [x] T028 [US2] In `docusaurus-book-site/src/components/chatbot/chatbot.module.css`, add styles for the message list, user messages, bot messages, and the "Thinking..." indicator, following the robotics theme.

**Checkpoint**: User Story 2 is functional. Users can have a simulated conversation.

---

## Phase 4: Polish & Documentation

**Purpose**: Finalize styling, responsiveness, and documentation.

- [x] T029 [P] In `docusaurus-book-site/src/components/chatbot/chatbot.module.css`, define and apply the full robotics theme, including the neon-cyan/electric-blue colors, Orbitron/Inter fonts, circuit-line borders, and AI-mesh background.
- [x] T030 Review and refine all styles for responsiveness on tablet and mobile devices.
- [x] T031 [P] Create a `README.md` file in `docusaurus-book-site/src/components/chatbot/`.
- [x] T032 In the new `README.md`, document the component structure, state management, and how to customize the theme. Clearly mark the `setTimeout` as the placeholder for future API integration.
- [x] T033 Manually test all acceptance criteria from the `spec.md` and verify all tasks are complete. (Requires manual verification by user)

---

## Dependencies & Execution Order

-   **Phase 1 (Setup)**: Must be completed first. All tasks within can be run in parallel.
-   **Phase 2 (User Story 1)**: Depends on Phase 1. Tasks should be done sequentially, though `T009-T011` can be done in parallel. `T018` and `T019` are the final integration steps for this phase.
-   **Phase 3 (User Story 2)**: Depends on Phase 2. `T020` and `T021` can be done in parallel. The rest depend on the state logic in `T022`.
-   **Phase 4 (Polish)**: Depends on all previous phases. Tasks can be done in parallel.

### Implementation Strategy: MVP First

1.  Complete **Phase 1**.
2.  Complete **Phase 2** to deliver the MVP: a visible chatbot widget that can be opened and closed.
3.  Complete **Phase 3** to add interactive functionality.
4.  Complete **Phase 4** for final polish and documentation.
