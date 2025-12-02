ID: 007
TITLE: Create Implementation Plan for Chat Search, Highlighting & Context Injection UI
STAGE: plan
DATE_ISO: 2025-12-02
SURFACE: agent
MODEL: gemini-1.5-pro
FEATURE: 007-chat-context-highlighting
BRANCH: 007-chat-context-highlighting
USER: user
COMMAND: /sp.plan

Create a detailed implementation plan for Feature 2.5 — Chat Search, Highlighting & Context Injection UI.

STRICT SAFETY REQUIREMENTS:
- Do NOT delete, modify, overwrite, or restructure any existing files, directories, branches, configs, or code from prior features.
- All work must be fully additive, using new files, new folders, or new isolated components.
- Existing chatbot UI, backend API, and agent logic must remain untouched except through additive integrations (e.g., new props, new modules, new extension hooks).

---------------------------------------------------------------------
PLAN SCOPE:
Design a complete step-by-step blueprint to introduce text selection, highlight UI, contextual query injection, metadata flow, and agent context prioritization.

Break the work into the following phases:

=====================================================================
PHASE 1 — Text Selection Detection Layer
=====================================================================
1. Create a new selection-detection module:
   - File: `src/ai/hooks/useTextSelection.js`
   - Responsibilities:
     • Listen for DOM text selections on all Docusaurus documentation pages  
     • Extract selected text  
     • Extract chapter/page ID  
     • Extract anchor/section ID when available  
     • Compute character offsets  
   - Sanitize selected text
   - Enforce maximum selection length (e.g., 2,000 chars)

2. Auto-clear selection when user navigates or clicks elsewhere.

=====================================================================
PHASE 2 — Highlighting & Robotics-Themed UI Interaction
=====================================================================
1. Create a floating “Ask About This” action component:
   - File: `src/ai/components/AskAboutThis.jsx`
   - Behavior:
     • Appears when user selects text  
     • Positioned near the selection  
     • Uses robotics neon-cyan color scheme  
     • Mobile-friendly repositioning  

2. Apply selection highlight overlay:
   - Create a CSS module with:
     • Neon blue glow  
     • Subtle grid pattern  
     • 8–12px border radius  

=====================================================================
PHASE 3 — Context Bubble Integration in Chat Panel
=====================================================================
1. Create a reusable Context Bubble component:
   - File: `src/ai/components/ContextBubble.jsx`
   - Shows selected text snippet inside the chatbot panel
   - Includes:
     • Expand/collapse  
     • Remove context button  
     • Scrollable long-text view  

2. Integrate bubble additively with chatbot UI:
   - New integration layer: `src/ai/chat/contextIntegration.js`
   - Must NOT modify existing chat UI files directly.
   - Use props, extension APIs, or plugin-style injection.

=====================================================================
PHASE 4 — Frontend → Backend Metadata Pipeline
=====================================================================
1. Extend existing chat request builder (additive only):
   - Add fields:
     • `selectedText`  
     • `chapterId`  
     • `sectionId`  
     • `offsets`  

2. Metadata is appended to requests without altering existing request content.

3. Ensure metadata supports existing streaming pipeline (Feature 2.4).

=====================================================================
PHASE 5 — Backend Metadata Processing (Additive Utilities)
=====================================================================
1. Add a new utility:
   - File: `server/utils/metadataInjector.js`
   - Responsibilities:
     • Validate incoming metadata  
     • Strip unsafe HTML  
     • Limit maximum length  
     • Attach metadata to agent request payload  

2. No modification to existing backend routes; only attach new middleware or helper modules.

=====================================================================
PHASE 6 — Agent Context Prioritization
=====================================================================
1. Modify agent to prioritize `selectedText`:
   - Identify agent's prompt construction logic.
   - Inject `selectedText` (and potentially `chapterId`, `sectionId`) directly into the agent's prompt with higher weighting or explicit instruction.
   - Ensure "If `selectedText` is provided, answer using ONLY this text unless user explicitly requests additional context" rule is enforced.

2. Update RAG retrieval based on context:
   - If `chapterId` and `sectionId` are present, filter RAG search to relevant documents/chunks within those boundaries.
   - If `selectedText` is present, it should either be used as the primary query or highly weighted in the embedding generation process.

3. Ensure no modification to existing agent files; only additive updates (new functions, new prompts, new modules).
LABELS: ["feature-planning"]
LINKS:
  SPEC: specs/007-chat-context-highlighting/spec.md
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - specs/007-chat-context-highlighting/plan.md
  - specs/007-chat-context-highlighting/research.md
  - specs/007-chat-context-highlighting/data-model.md
  - specs/007-chat-context-highlighting/contracts/chat_request_extension.md
  - specs/007-chat-context-highlighting/quickstart.md
TESTS_YAML: []
PROMPT_TEXT: |
  /sp.plan

  Create a detailed implementation plan for Feature 2.5 — Chat Search, Highlighting & Context Injection UI.

  STRICT SAFETY REQUIREMENTS:
  - Do NOT delete, modify, overwrite, or restructure any existing files, directories, branches, configs, or code from prior features.
  - All work must be fully additive, using new files, new folders, or new isolated components.
  - Existing chatbot UI, backend API, and agent logic must remain untouched except through additive integrations (e.g., new props, new modules, new extension hooks).

  ---------------------------------------------------------------------
  PLAN SCOPE:
  Design a complete step-by-step blueprint to introduce text selection, highlight UI, contextual query injection, metadata flow, and agent context prioritization.

  Break the work into the following phases:

  =====================================================================
  PHASE 1 — Text Selection Detection Layer
  =====================================================================
  1. Create a new selection-detection module:
     - File: `src/ai/hooks/useTextSelection.js`
     - Responsibilities:
       • Listen for DOM text selections on all Docusaurus documentation pages  
       • Extract selected text  
       • Extract chapter/page ID  
       • Extract anchor/section ID when available  
       • Compute character offsets  
     - Sanitize selected text
     - Enforce maximum selection length (e.g., 2,000 chars)

  2. Auto-clear selection when user navigates or clicks elsewhere.

  =====================================================================
  PHASE 2 — Highlighting & Robotics-Themed UI Interaction
  =====================================================================
  1. Create a floating “Ask About This” action component:
     - File: `src/ai/components/AskAboutThis.jsx`
     - Behavior:
       • Appears when user selects text  
       • Positioned near the selection  
       • Uses robotics neon-cyan color scheme  
       • Mobile-friendly repositioning  

  2. Apply selection highlight overlay:
     - Create a CSS module with:
       • Neon blue glow  
       • Subtle grid pattern  
       • 8–12px border radius  

  =====================================================================
  PHASE 3 — Context Bubble Integration in Chat Panel
  =====================================================================
  1. Create a reusable Context Bubble component:
     - File: `src/ai/components/ContextBubble.jsx`
     - Shows selected text snippet inside the chatbot panel
     - Includes:
       • Expand/collapse  
       • Remove context button  
       • Scrollable long-text view  

  2. Integrate bubble additively with chatbot UI:
     - New integration layer: `src/ai/chat/contextIntegration.js`
     - Must NOT modify existing chat UI files directly.
     - Use props, extension APIs, or plugin-style injection.

  =====================================================================
  PHASE 4 — Frontend → Backend Metadata Pipeline
  =====================================================================
  1. Extend existing chat request builder (additive only):
     - Add fields:
       • `selectedText`  
       • `chapterId`  
       • `sectionId`  
       • `offsets`  

  2. Metadata is appended to requests without altering existing request content.

  3. Ensure metadata supports existing streaming pipeline (Feature 2.4).

  =====================================================================
  PHASE 5 — Backend Metadata Processing (Additive Utilities)
  =====================================================================
  1. Add a new utility:
     - File: `server/utils/metadataInjector.js`
     - Responsibilities:
       • Validate incoming metadata  
       • Strip unsafe HTML  
       • Limit maximum length  
       • Attach metadata to agent request payload  

  2. No modification to existing backend routes; only attach new middleware or helper modules.

  =====================================================================
  PHASE 6 — Agent Context Prioritization
  =====================================================================
  1. Modify agent to prioritize `selectedText`:
     - Identify agent's prompt construction logic.
     - Inject `selectedText` (and potentially `chapterId`, `sectionId`) directly into the agent's prompt with higher weighting or explicit instruction.
     - Ensure "If `selectedText` is provided, answer using ONLY this text unless user explicitly requests additional context" rule is enforced.

  2. Update RAG retrieval based on context:
     - If `chapterId` and `sectionId` are present, filter RAG search to relevant documents/chunks within those boundaries.
     - If `selectedText` is present, it should either be used as the primary query or highly weighted in the embedding generation process.

  3. Ensure no modification to existing agent files; only additive updates (new functions, new prompts, new modules).
RESPONSE_TEXT: |
  The implementation plan for "Chat Search, Highlighting & Context Injection UI" (Feature 2.5) has been successfully created.

  **Branch Name**: `007-chat-context-highlighting`
  **Plan File Path**: `specs/007-chat-context-highlighting/plan.md`

  **Generated Artifacts:**
  *   `specs/007-chat-context-highlighting/research.md`
  *   `specs/007-chat-context-highlighting/data-model.md`
  *   `specs/007-chat-context-highlighting/contracts/chat_request_extension.md`
  *   `specs/007-chat-context-highlighting/quickstart.md`

  The agent's context (`GEMINI.md`) has also been updated with relevant information from the plan, including the identified database (Qdrant) and project type.

  You can now proceed with `/sp.tasks` to break down this plan into actionable tasks.
OUTCOME: Implementation plan and supporting design artifacts for Feature 2.5 created. Agent context updated.
EVALUATION: The plan is complete and ready for task breakdown.
