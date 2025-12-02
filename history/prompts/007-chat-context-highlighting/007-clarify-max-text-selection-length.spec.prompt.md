ID: 007
TITLE: Clarify Max Text Selection Length
STAGE: spec
DATE_ISO: 2025-12-02
SURFACE: agent
MODEL: gemini-1.5-pro
FEATURE: 007-chat-context-highlighting
BRANCH: 007-chat-context-highlighting
USER: user
COMMAND: /sp.specify Feature 2.5 — Chat Search, Highlighting & Context Injection UI Goal: Implement user-selectable text highlighting inside the Docusaurus book and enable “Ask About This” contextual queries. Selected text must flow from the frontend → backend → agent → response stream, allowing the assistant to answer questions based strictly on user-selected content. Safety Rule: This feature must be *fully additive*. It must not delete, modify, or overwrite any existing project files, folders, branches, or data. ############################################################### ################### FUNCTIONAL REQUIREMENTS ############### ############################################################### 1. Text Selection Capture - Detect text selection across all Docusaurus documentation pages. - Extract: • Selected text • Chapter/page ID • Section anchor (if available) • Character start/end offsets - Normalize and sanitize selected text to prevent HTML/script injection. - Limit maximum selection length for performance and safety. 2. UI Highlighting System - Apply a subtle robotics-themed highlight (electric blue / neon cyan). - Support: • Single-selection mode • Automatic clearing when new text is selected - Visual “context capture” indicator. 3. “Ask About This” Action Button - When text is selected, a floating context menu or tooltip appears: → Button: **Ask About This** - On click: • Send selection metadata + text to chatbot panel • Auto-open chatbot if closed • Prefill context in the input box or context pill • Prepare backend metadata payload 4. Context Panel in Chat UI - Display selected text as a **Context Bubble** above the user query box. - Allow user to: • Remove context • Edit context (optional) • Expand/collapse long context snippets - Robotics UI theme: grid-lines, soft blue neon edges. 5. Metadata Pipeline Integration - Selected text must be passed to the backend with: • `selectedText` • `chapterId` • `sectionId` • `offsets` - Backend must attach metadata untouched to agent’s RAG retrieval step. 6. Backend Safety - Do not modify or delete any existing routes/endpoints. - Add new supporting metadata utilities only if needed. - Sanitize selected text: • Strip HTML • Limit length • Prevent injection 7. Agent-Level Integration - Agent should use metadata as higher-priority context than regular RAG. - Instructions: • “If `selectedText` is provided, answer using ONLY this text unless user explicitly requests additional context.” - No modification to existing agent files — only additive updates (new functions, new prompts, new modules). 8. Frontend–Backend Streaming Integrity - The existing streamed response system from Feature 2.4 must continue to operate without modification. - This feature must integrate selected context into existing streaming flow via additive parameters. ############################################################### ######################## UI REQUIREMENTS ################### ############################################################### 1. Robotics-Aligned Theme - Neon blue accent color - Rounded corners (8px–12px) - Subtle grid background pattern on context bubble - Soft glow hover effects 2. Floating Action UI - “Ask About This” button must: • Float near selected text • Auto-position according to viewport • Have mobile-friendly behavior 3. Accessibility - Keyboard navigation friendly - High-contrast text - Screen-reader announcements: • “Text selected” • “Context applied to chatbot”
LABELS: ["feature-specification", "clarification"]
LINKS:
  SPEC: specs/007-chat-context-highlighting/spec.md
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - specs/007-chat-context-highlighting/checklists/requirements.md
  - specs/007-chat-context-highlighting/spec.md
TESTS_YAML: []
PROMPT_TEXT: |
  A
RESPONSE_TEXT: |
  I have updated the spec.md file with the user's clarification.

  Now I will report the completion.

  **Completion Report:**

  The feature specification for "Chat Search, Highlighting & Context Injection UI" has been successfully created.

  **Branch Name**: `007-chat-context-highlighting`
  **Spec File Path**: `specs/007-chat-context-highlighting/spec.md`
  **Checklist File Path**: `specs/007-chat-context-highlighting/checklists/requirements.md`

  All functional and UI requirements, user scenarios, and success criteria have been documented. The clarification regarding the maximum text selection length (1000 characters) has been incorporated into the specification.

  You can now proceed with `/sp.plan` to begin planning the implementation of this feature.
OUTCOME: User chose 1000 characters for max text selection length. Spec updated.
EVALUATION: The feature specification is complete and ready for planning.
