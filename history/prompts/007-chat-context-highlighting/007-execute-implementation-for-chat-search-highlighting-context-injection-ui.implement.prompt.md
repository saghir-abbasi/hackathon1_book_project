ID: 007
TITLE: Execute Implementation for Chat Search, Highlighting & Context Injection UI
STAGE: implement
DATE_ISO: 2025-12-02
SURFACE: agent
MODEL: gemini-1.5-pro
FEATURE: 007-chat-context-highlighting
BRANCH: 007-chat-context-highlighting
USER: user
COMMAND: /sp.implement

Feature 2.5 — Chat Search, Highlighting & Context Injection UI

SAFE EXECUTION RULES:
- Must NOT delete, modify, overwrite, or restructure any existing project files, folders, branches, or configurations.
- All new code must be additive. You may create new files or extend existing files **safely** without removing previous logic.
- Existing Chatbot UI (Feature 2.1/2.2), backend APIs (Feature 2.3), and OpenAI Agent integration (Feature 2.4) must remain untouched.

---

## 1. FRONTEND IMPLEMENTATION (Additive Only)

### 1.1 Text Selection Hook
- File: `/src/ai/hooks/useTextSelection.js`
- Responsibilities:
  - Detect text selection in all Docusaurus pages
  - Extract selected text, chapterId, sectionId, character offsets
  - Sanitize input (strip HTML/script)
  - Cap maximum selection length (e.g., 2,000 chars)
  - Provide a cleanup mechanism on navigation or deselection

### 1.2 Highlighting & “Ask About This” Button
- File: `/src/ai/components/AskAboutThis.jsx`
- Responsibilities:
  - Appear near selected text
  - Show floating button with robotics-themed neon blue highlight
  - Mobile-responsive placement
  - Click triggers sending metadata + text to Chatbot panel
- File: `/src/ai/components/ContextBubble.jsx`
  - Displays selected text context in chatbot panel
  - Expand/collapse long snippets
  - Remove context option
  - Soft glow + grid-themed background consistent with robotics UI

### 1.3 Context Integration Layer
- File: `/src/ai/chat/contextIntegration.js`
- Responsibilities:
  - Integrate ContextBubble with existing Chatbot UI additively
  - Forward metadata (`selectedText`, `chapterId`, `sectionId`, offsets) to backend request
  - Must **not** overwrite existing frontend logic
  - Maintain existing streamed response flow

---

## 2. BACKEND SUPPORT (Additive Only)

### 2.1 Metadata Injector Utility
- File: `/server/utils/metadataInjector.js`
- Responsibilities:
  - Validate incoming metadata
  - Sanitize selected text
  - Enforce character length limits
  - Append metadata safely to agent request payload
  - Must **not** alter existing API routes

### 2.2 Agent Prompt Extension
- File: `/server/agent/contextPromptExtension.js`
- Responsibilities:
  - If `selectedText` exists, prepend instructions to agent prompt:  
    “Answer using only the selected text unless user explicitly requests additional context.”
  - Additive only; no changes to existing agent files

---

## 3. STREAMING INTEGRATION

- Ensure selected text metadata flows through the **existing streaming pipeline** (Feature 2.4) without breaking token-by-token delivery
- Maintain heartbeat, reconnect, and retry logic from previous features
- No modification to existing SSE or frontend streaming hooks

---

## 4. UI & UX

- Robotics-themed color scheme: neon blue / cyan
- Rounded corners 8–12px
- Grid pattern or soft glow effect for context bubbles
- Floating button placement responsive to viewport
- Keyboard-accessible and screen-reader friendly
- Toast notification or subtle animation for “Context applied” event

---

## 5. VALIDATION CHECKLIST

- User can select text → click “Ask About This” → chatbot receives context
- Context flows frontend → backend → agent → streamed response
- Agent prioritizes selected text correctly
- No existing files, branches, or data are deleted or modified
- All additions are additive and non-destructive
- Frontend and backend builds successfully without errors

---

# END OF /sp.implement — FEATURE 2.5
RESPONSE_TEXT: |
  The implementation tasks for "Chat Search, Highlighting & Context Injection UI" (Feature 2.5) have been processed and executed.

  **Branch Name**: `007-chat-context-highlighting`
  **Tasks File Path**: `specs/007-chat-context-highlighting/tasks.md`

  All tasks have been marked as complete. This includes:
  *   Phase 1: Setup (installing frontend/backend sanitization libraries, extending backend data model)
  *   Phase 2: User Story 1 (Frontend text selection, UI highlighting, floating action button, frontend-backend metadata pipeline extension, backend metadata processing, agent context prioritization)
  *   Phase 3: User Story 2 (Frontend context bubble integration)
  *   Phase 4: Polish & Cross-Cutting Concerns (updating quickstart, adding tests, documentation, end-to-end testing)

  The primary development work for this feature is now complete. You can proceed with verifying the functionality according to the `quickstart.md` and conducting further testing.
OUTCOME: All implementation tasks for Feature 2.5 have been executed.
EVALUATION: The feature has been implemented as per the plan.
