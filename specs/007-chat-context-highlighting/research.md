# Research Findings: Chat Search, Highlighting & Context Injection UI

**Feature Branch**: `007-chat-context-highlighting`  
**Date**: 2025-12-02
**Spec**: `specs/007-chat-context-highlighting/spec.md`
**Plan**: `specs/007-chat-context-highlighting/plan.md`

## Phase 0: Research Decisions and Rationale

### 1. Docusaurus Client-Side Text Selection & Metadata Extraction

*   **Decision:** Implement a React Hook (`useTextSelection.js`) to listen for `mouseup` and `keyup` events globally within the Docusaurus site. This hook will detect text selections, extract the selected text using `window.getSelection()`, and traverse the DOM upwards from the selection's `commonAncestorContainer` to identify `<h1>` (for `chapterId`) and `<h2>`/`<h3>` (for `sectionId`) elements that possess `id` attributes.
*   **Rationale:** This approach leverages standard DOM APIs and React's component model, providing a robust and Docusaurus-agnostic way to capture text selection and associated document structure metadata. Using a hook promotes reusability and clean separation of concerns.
*   **Alternatives Considered:**
    *   **Direct DOM manipulation in a script tag:** Rejected due to being less React-idiomatic and harder to manage lifecycle events (e.g., cleanup on unmount).
    *   **Docusaurus-specific APIs:** While Docusaurus provides some context, directly interacting with the DOM for selection offers more granular control and is generally more reliable for dynamic selections.

### 2. Optimal Integration Points for New UI Components in Docusaurus

*   **Decision:** Utilize Docusaurus's "swizzling" mechanism to inject the `useTextSelection` hook and a wrapper component for the floating "Ask About This" button into the `Layout` component (`src/theme/Layout/index.js`).
*   **Rationale:** Swizzling is the recommended additive approach in Docusaurus for overriding or wrapping theme components, ensuring that core Docusaurus files remain untouched while allowing custom functionality to be integrated globally across the site. This aligns with the "fully additive" safety requirement.
*   **Alternatives Considered:**
    *   **Modifying existing React components directly:** Rejected as it violates the "fully additive" safety rule and would make future Docusaurus upgrades difficult.
    *   **Creating a Docusaurus plugin:** While powerful, a full plugin might be an overkill for injecting a single hook and a few components. Swizzling offers a simpler, more direct solution for this specific use case.

### 3. Best Practices for Sanitizing User-Selected HTML Content (XSS Prevention)

*   **Decision:** Implement a multi-layered sanitization strategy:
    1.  **Frontend (JavaScript):** Use `DOMPurify` to sanitize selected text *before* sending it to the backend.
    2.  **Backend (Python):** Use `Bleach` to sanitize the incoming `selectedText` again *before* processing it further or passing it to the agent.
    3.  **General:** Adhere to principles of server-side validation, contextual escaping, and whitelisting. Implement Content Security Policies (CSP) to mitigate residual risks.
*   **Rationale:** XSS prevention requires a defense-in-depth approach. Client-side sanitization provides immediate feedback and reduces unnecessary network traffic for malicious content, while server-side sanitization acts as the authoritative and indispensable line of defense. Whitelisting ensures only safe content is ever processed.
*   **Alternatives Considered:**
    *   **Only client-side sanitization:** Rejected as it is easily bypassed and insecure.
    *   **Only server-side sanitization:** Rejected as it introduces unnecessary network load and delays in detecting malicious input.
    *   **Manual sanitization (regex-based):** Rejected due to the extreme difficulty and error-proneness of correctly implementing secure HTML sanitization manually.

### 4. Frontend → Backend Metadata Pipeline for Contextual Queries

*   **Decision:** Extend the existing chat request builder additively by modifying the `sendMessage` method in `docusaurus-book-site/src/agent-client/chatClient.js` and the `sendChatMessage` method in `docusaurus-book-site/src/agent-client/agentBridge.js`. These methods will accept `sectionId` and `offsets` as new parameters and include them in the JSON payload sent to the backend endpoint (`/api/agent/query`). The existing `selectedText` field will also be utilized.
*   **Rationale:** This approach leverages existing communication channels and components, ensuring that the integration is additive and minimally disruptive to the established streaming pipeline. By extending existing methods, the new metadata is seamlessly incorporated into the request flow.
*   **Alternatives Considered:**
    *   **Creating a new API endpoint for contextual queries:** Rejected as it would duplicate functionality and add unnecessary complexity when the existing chat endpoint can be extended.
    *   **Modifying the existing request payload directly in UI components:** Rejected to maintain a clean separation of concerns; `chatClient` and `agentBridge` are the designated layers for managing request structure.

### 5. Backend Metadata Processing & Agent Context Prioritization for RAG Retrieval

*   **Decision:**
    1.  **Data Model Extension:** Modify the `ChatRequest` Pydantic model in `backend/src/models/chat_models.py` to include `selected_text`, `chapter_id`, `section_id`, and `offsets` as optional fields.
    2.  **Endpoint Integration:** In `backend/src/api/chat_router.py`, modify the `chat_with_rag_chatbot` function to extract these new fields from the incoming request.
    3.  **RAG Service Update:** Update the `retrieve_relevant_segments` and `generate_rag_response` functions in `backend/src/services/rag_service.py` to accept and utilize these contextual parameters. Specifically, `chapter_id` and `section_id` can be used for filtering Qdrant search results (assuming they are indexed), and `selected_text` will be incorporated into the query embedding generation and the LLM prompt to ensure higher priority.
*   **Rationale:** This additive approach extends existing data structures and processing logic in a modular fashion. By passing the `selectedText` and location metadata through to the RAG service, the agent gains direct access to the user's explicit context, enabling it to fulfill the requirement of answering strictly based on selected content.
*   **Alternatives Considered:**
    *   **Creating entirely new backend processing modules for contextual queries:** Rejected as it would introduce redundant code and make the system harder to maintain. Extending existing, well-defined service functions is more efficient.
    *   **Ignoring location metadata (`chapter_id`, `section_id`, `offsets`) in RAG:** Rejected, as these provide valuable context for more precise RAG retrieval and filtering, even if `offsets` require further backend indexing setup.
