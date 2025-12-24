# Feature Specification: Feature 2.4 — OpenAI Agents / ChatKit Integration

**Feature Branch**: `006-openai-agent-integration`  
**Created**: December 2, 2025  
**Status**: Draft  
**Input**: User description: "Feature 2.4 — OpenAI Agents / ChatKit Integration Objective: Implement a complete intelligent agent layer that bridges: (1) the Docusaurus frontend, (2) the FastAPI backend from Feature 2.3, (3) the OpenAI Agents / ChatKit SDK system. The result must be a fully operational, streamed-response AI assistant capable of answering queries using the book’s knowledge via RAG. All implementation MUST be additive and MUST NOT modify or delete any previous project data, branches, or files. --- ## Functional Requirements ### 1. Agent Definition - Create an Agent definition (JSON or Python class) inside `backend/app/agent/`. - Agent should include: • Name, description • System prompt tuned to the book • Personality = Formal, technical, robotics-themed • Context window settings • Allowed tools and safety constraints - System prompt must support: • Physical AI & Humanoid Robotics knowledge • ROS 2, Gazebo, Unity simulations • NVIDIA Isaac, VLA systems • Book content extraction from RAG ### 2. Tools Configuration - Configure tools the agent will use: • RAG tool — Uses Qdrant vector search from Feature 2.3 • Selected-text extraction tool — Provided by frontend • Book chapter metadata tool • Optional session logging tool - Each tool must be implemented as a function in `backend/app/agent/tools/`. - Tools must return JSON-serializable outputs. ### 3. Binding RAG Function to the Agent - Provide a function `rag_query(query)` bound into agent tools. - Internally call: • vector search (Qdrant) • Neon DB for chat/session awareness • returns top-k segments - Ensure no destruction of existing DB data. ### 4. System Prompts Tuned to the Book - Create `system_prompts/primary.txt` in agent folder. - Content includes: • Embodied AI principles • Robotics pipeline • ROS 2 → Gazebo → Isaac → VLA • Constraints: Answers must come from book + RAG • Maintain professional tone ### 5. Client-Side SDK Integration (ChatKit/OpenAI JS) - Implement JS client interface inside Docusaurus plugin folder: • `chatClient.js` • Use OpenAI ChatCompletions or ChatKit client • Must use streaming mode (Server-Sent Events or fetch streams) - Client must pass: • user query • selected text • chapter ID • session token - Streaming must integrate into the existing chat window without modifying old UI code. ### 6. Streamed Responses - Backend must expose `/agent/stream` SSE or chunked streaming endpoint. - Backend consumes: • user prompt • metadata • RAG output - Streams tokens to frontend. ### 7. Reconnect & Retry Logic - Implement safe reconnect logic: • retry if stream breaks • resume gracefully - Timeout behavior: auto-cancel after configurable duration. ### 8. Metadata Injection - All queries MUST automatically include: • chapter ID • selected text range • user session • last model messages - Metadata forwarded to RAG and Agent. ### 9. Security & API Key Management - Store API keys inside **backend/.env** only. - Never expose keys to frontend. - Use backend server-to-server secure calls. - Input sanitization for: • prompt text • metadata values • user IDs ### 10. Abuse Prevention Implement: - rate limiting per session - prompt length checks • metadata boundaries • “selected text” size caps • output token caps ### 11. Frontend → Backend → Agent Bridge - The pipeline must work as: Docusaurus UI → Chat SDK wrapper → `/agent/stream` → Agent reasoning + RAG → Streamed tokens → UI renderer - No changes to previous components except additive files. ### 12. Safe Execution Constraints - Do NOT delete or overwrite any existing: • book content • Docusaurus files • backend folders (Feature 2.3)"

## User Scenarios & Testing

### User Story 1 - Ask a Question to the AI Assistant (Priority: P1)

As a user, I want to ask questions about the book's content through a chat interface so that I can quickly get relevant information.

**Why this priority**: This is the core functionality of the AI assistant, providing direct value to the user by enabling quick access to book knowledge.

**Independent Test**: This can be fully tested by interacting with the chat interface, submitting a question, and verifying that a streamed, contextually relevant response is received.

**Acceptance Scenarios**:

1.  **Given** the Docusaurus site is open and the chat interface is available, **When** a user types a question and submits it, **Then** the user sees a streamed, contextually relevant response based on the book's knowledge.
2.  **Given** a chapter is open and the user has selected text, **When** the user asks a question related to the selected text, **Then** the AI assistant provides an answer that demonstrates an understanding of the selected text and the broader book content.

### User Story 2 - AI Assistant Handles Disconnected Stream (Priority: P2)

As a user, I want the chat experience to be resilient to network interruptions so that my conversation is not lost and I can continue interacting with the AI assistant.

**Why this priority**: Ensures a robust and reliable user experience, especially in environments with unstable network connectivity.

**Independent Test**: This can be tested by simulating network disconnections during an active streaming response and observing the system's ability to recover or inform the user.

**Acceptance Scenarios**:

1.  **Given** a chat session is active and a response is streaming, **When** the network connection is temporarily interrupted, **Then** the system attempts to reconnect and resume the streamed response gracefully.
2.  **Given** a chat session is active and a response is streaming, **When** the network connection is lost beyond a configurable duration, **Then** the system automatically cancels the stream and informs the user of the timeout, allowing them to initiate a new query.

### User Story 3 - AI Assistant Uses Configured Tools (Priority: P2)

As a user, I want the AI assistant to leverage its internal tools, such as the RAG system, to provide comprehensive and accurate answers from the book's content.

**Why this priority**: Validates the agent's ability to utilize its configured tools for enhanced information retrieval and accurate responses.

**Independent Test**: This can be tested by posing questions that specifically require the RAG tool to retrieve information that is not part of the agent's base knowledge but is present in the book content.

**Acceptance Scenarios**:

1.  **Given** the AI assistant is configured with a RAG tool for Qdrant vector search, **When** a user asks a question requiring information from the book, **Then** the AI assistant uses the RAG tool to retrieve relevant segments from the book and incorporates them into its response.
2.  **Given** the AI assistant is provided with a chapter ID and selected text, **When** it processes a user query, **Then** the AI assistant utilizes these metadata to refine its understanding and response through its tools.

### Edge Cases

-   What happens when the RAG tool returns no relevant segments for a user's query?
-   How does the system handle an invalid, expired, or missing API key for external services?
-   What happens if the user's query text, selected text, or metadata values exceed the defined length or boundary caps?
-   How does the system respond if the agent fails to generate a response due to internal errors (e.g., model errors) or content moderation filters?
-   What is the behavior if the Frontend to Backend communication is interrupted during metadata injection or streaming initiation?

## Requirements

### Functional Requirements

-   **FR-AGENT-001**: The system MUST define an AI Assistant component, characterized by: a Name, description, a System prompt tuned to the book's domain, a Formal, technical, robotics-themed Personality, configurable Context window settings, and a list of Allowed tools and safety constraints.
-   **FR-AGENT-002**: The Agent's system prompt MUST support knowledge areas: Physical AI & Humanoid Robotics, ROS 2, Gazebo, Unity simulations, NVIDIA Isaac, VLA systems, and Book content extraction via RAG.
-   **FR-TOOLS-001**: The AI Assistant MUST be configurable with a set of tools, including: a Retrieval Augmented Generation (RAG) tool for knowledge retrieval, a Selected-text extraction tool to process user-highlighted content, a Book chapter metadata tool, and an Optional session logging tool.
-   **FR-TOOLS-002**: Each AI Assistant tool MUST be implemented as a distinct, callable capability.
-   **FR-TOOLS-003**: All agent tools MUST return JSON-serializable outputs.
-   **FR-RAG-001**: The agent MUST include a function `rag_query(query)` bound into its tools.
-   **FR-RAG-002**: The RAG query function MUST internally perform semantic search for relevant information and interact with a session management system for chat awareness, returning relevant segments.
-   **FR-RAG-003**: The RAG implementation MUST NOT destroy any existing database data.
-   **FR-PROMPT-001**: The AI Assistant MUST utilize a primary system prompt that defines its persona and operational guidelines, encompassing: Embodied AI principles, the Robotics pipeline (e.g., ROS 2, Gazebo, Isaac, VLA), constraints (answers must come from book + RAG), and a professional tone.
-   **FR-CLIENT-001**: A client-side chat interface component MUST be implemented within the content delivery platform's extension mechanism.
-   **FR-CLIENT-002**: The client interface MUST communicate with the AI Assistant using a standard messaging protocol.
-   **FR-CLIENT-003**: The client interface MUST operate in streaming mode (Server-Sent Events or fetch streams).
-   **FR-CLIENT-004**: The client MUST pass: user query, selected text, chapter ID, and session token to the backend.
-   **FR-CLIENT-005**: Streaming MUST integrate into the existing chat window without modifying old UI code.
-   **FR-BACKEND-001**: The backend server MUST provide a dedicated streaming endpoint for AI Assistant interactions.
-   **FR-BACKEND-002**: The `/agent/stream` endpoint MUST consume: user prompt, metadata, and RAG output.
-   **FR-BACKEND-003**: The backend MUST stream tokens to the frontend.
-   **FR-RECONNECT-001**: The system MUST implement safe reconnect logic, retrying if the stream breaks and resuming gracefully.
-   **FR-RECONNECT-002**: The system MUST implement timeout behavior, automatically canceling the stream after a configurable duration.
-   **FR-METADATA-001**: All queries MUST automatically include: chapter ID, selected text range, user session, and last model messages.
-   **FR-METADATA-002**: All injected metadata MUST be forwarded to both the RAG system and the Agent.
-   **FR-SECURITY-001**: API keys MUST be stored securely within the backend's environment configuration.
-   **FR-SECURITY-002**: API keys MUST NEVER be exposed to the frontend.
-   **FR-SECURITY-003**: The system MUST use backend server-to-server secure calls for external API interactions.
-   **FR-SECURITY-004**: Input sanitization MUST be applied for: prompt text, metadata values, and user IDs.
-   **FR-ABUSE-001**: The system MUST implement rate limiting per session.
-   **FR-ABUSE-002**: The system MUST implement prompt length checks.
-   **FR-ABUSE-003**: The system MUST implement metadata boundaries.
-   **FR-ABUSE-004**: The system MUST implement “selected text” size caps.
-   **FR-ABUSE-005**: The system MUST implement output token caps.
-   **FR-BRIDGE-001**: The overall interaction pipeline MUST facilitate communication from the User Interface (UI), through an integration layer, to the backend's streaming endpoint, which then integrates AI Assistant reasoning and knowledge retrieval to deliver streamed responses back to the UI.
-   **FR-CONSTRAINTS-001**: All implementation MUST be additive and MUST NOT delete or overwrite any existing book content, existing frontend assets, or existing backend components.

### Key Entities

-   **User**: An individual interacting with the Docusaurus book site.
-   **Chat Session**: A continuous conversation between a User and the AI Assistant, identified by a session token, and maintaining message history and context.
-   **AI Assistant (Agent)**: The intelligent layer responsible for processing user queries, reasoning, utilizing tools, and generating responses.
-   **RAG Tool**: An internal tool used by the AI Assistant to perform vector searches on Qdrant and retrieve relevant book segments.
-   **Selected-Text Extraction Tool**: An internal tool that processes text highlighted by the user in the frontend to provide additional context to the AI Assistant.
-   **Book Chapter Metadata Tool**: An internal tool providing information about book chapters.
-   **FastAPI Backend**: The server-side application (from Feature 2.3) hosting the AI Agent, managing API keys, processing queries, and streaming responses.
-   **Docusaurus Frontend**: The client-side application (book website) displaying the chat UI, sending user inputs, and rendering streamed AI responses.
-   **Book Content**: The collection of textual data within the Docusaurus site that serves as the knowledge base for the RAG system.
-   **API Keys**: Credentials for accessing external services, securely managed by the backend.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: 90% of user queries result in a streamed, contextually relevant response from the AI assistant within 5 seconds.
-   **SC-002**: The AI assistant accurately incorporates information from selected text and chapter ID into its responses for 95% of queries where such context is provided and relevant.
-   **SC-003**: In cases of temporary network interruption during streaming, the chat interface successfully reconnects and resumes the response within 10 seconds for 80% of occurrences.
-   **SC-004**: API key management demonstrates complete security, ensuring no exposure to the frontend and all external service calls originate securely from the backend.
-   **SC-005**: Abuse prevention mechanisms (rate limiting, input/output caps) effectively prevent system overload and misuse, identified by monitoring logs for successful blocking of malicious attempts without impacting legitimate users.