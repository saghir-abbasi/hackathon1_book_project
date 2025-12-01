# Feature Specification: Backend API Layer (FastAPI + Qdrant + Neon)

**Feature Branch**: `001-rag-backend-api`  
**Created**: 2025-12-01  
**Status**: Draft  
**Input**: User description: "Feature: 2.3 — Backend API Layer (FastAPI + Qdrant + Neon) Objective: Develop the backend services for the RAG chatbot, including book content embedding, vector search, chat session handling, and database integration. All implementation must be **isolated and additive**, ensuring no existing frontend components, project files, or git branches are deleted or modified. Requirements: 1. FastAPI Server Setup - Create a new FastAPI project under a separate folder, e.g., `backend/`. - Implement the following API endpoints: • `/embed` — Accept book content chunks and store embeddings in Qdrant. • `/query` — Accept user questions and return relevant text chunks from Qdrant. • `/chat` — Accept user input, retrieve relevant context, and return assistant response. - Enable CORS for frontend Docusaurus integration. - **Do not modify any existing frontend components or files.** 2. Qdrant Vector Database Integration - Set up a Qdrant collection specifically for book embeddings. - Implement functions to: • `upsert` embeddings • `search` nearest neighbors for a query - Store connection credentials in a `.env` file. - **Ensure all work is isolated and additive, without touching previous project files.** 3. Neon Serverless PostgreSQL Integration - Create database tables for: • User sessions • Optional chat history for analytics - Implement database helper functions for inserting and retrieving session data. - Ensure schema changes are isolated and do not affect any existing databases or data. 4. RAG Pipeline Implementation - Implement the backend logic for: • Text chunking of book content • Generating embeddings using OpenAI or Claude Code embeddings • Vector search in Qdrant • Assembling assistant responses for the chatbot - All code should reside in `backend/` and not interfere with frontend mock responses. 5. Configuration & Environment Safety - Store all API keys, database URLs, and secrets in `.env` files. - Ensure no hard-coded credentials or changes to frontend configurations. - **The backend implementation must not overwrite any existing project data.** 6. Testing & Validation - Implement unit tests for each endpoint: • `/embed` — validate embeddings are stored correctly • `/query` — validate correct retrieval of text chunks • • `/chat` — validate response assembly - Simulate queries with dummy book content to ensure backend works independently. Deliverables: - Fully functional FastAPI backend with isolated folder structure. - Integration with Qdrant for embeddings and search. - Integration with Neon PostgreSQL for session management. - RAG pipeline ready for frontend integration. - All code additive, non-destructive to existing project files or git history. Non-Goals: - Do not connect to or modify existing frontend components. - Do not delete or overwrite previous mock frontend responses or project data. - Do not implement frontend rendering in this feature. End of specification."

## User Scenarios & Testing

### User Story 1 - Embed Book Content (Priority: P1)

As an administrator, I want to embed book content chunks into the vector database so that the chatbot can perform relevant searches.

**Why this priority**: Essential for the RAG chatbot's core functionality; without embedded content, the chatbot cannot provide informed responses.

**Independent Test**: Can be fully tested by providing book content chunks to the `/embed` endpoint and verifying that embeddings are stored in Qdrant.

**Acceptance Scenarios**:

1. **Given** raw book content chunks, **When** the content is sent to the `/embed` endpoint, **Then** the content is chunked, embedded, and stored in Qdrant successfully.
2. **Given** invalid or malformed book content, **When** it is sent to the `/embed` endpoint, **Then** the API returns an appropriate error message and does not store invalid embeddings.

### User Story 2 - Query Book Content (Priority: P1)

As a chatbot, I want to query the vector database with a user's question to retrieve relevant book content chunks, so that I can formulate an accurate answer.

**Why this priority**: Directly supports the chatbot's ability to answer user questions based on book content.

**Independent Test**: Can be fully tested by sending a user question to the `/query` endpoint and receiving relevant text chunks from Qdrant.

**Acceptance Scenarios**:

1. **Given** a user question, **When** the question is sent to the `/query` endpoint, **Then** the API returns relevant text chunks from the Qdrant database.
2. **Given** a query that yields no relevant results, **When** the query is sent to the `/query` endpoint, **Then** the API indicates that no relevant content was found.

### User Story 3 - Chat with RAG Chatbot (Priority: P1)

As a user, I want to ask questions to the chatbot and receive answers based on the book content, so that I can learn more about the topics.

**Why this priority**: This is the primary user interaction with the RAG chatbot.

**Independent Test**: Can be fully tested by sending user input to the `/chat` endpoint and receiving an assistant response based on retrieved context.

**Acceptance Scenarios**:

1. **Given** a user input, **When** the input is sent to the `/chat` endpoint, **Then** the API retrieves relevant context from Qdrant and returns an assembled assistant response.
2. **Given** a chat session, **When** multiple turns of conversation occur, **Then** the chat history (if enabled) is managed in the PostgreSQL database.
3. **Given** a user input that requires external knowledge beyond the book, **When** the input is sent to the `/chat` endpoint, **Then** the API provides a helpful response or indicates limitations without hallucinating.

### User Story 4 - Manage Chat Sessions (Priority: P2)

As an administrator, I want chat sessions and optional chat history to be stored and managed in the PostgreSQL database for analytics and continuity.

**Why this priority**: Important for understanding user engagement and improving the chatbot over time.

**Independent Test**: Can be fully tested by verifying that user session data and chat history are correctly stored and retrieved from the Neon PostgreSQL database after chat interactions.

**Acceptance Scenarios**:

1. **Given** a new chat session, **When** the session begins, **Then** a new user session entry is created in the PostgreSQL database.
2. **Given** chat interactions, **When** chat history is enabled, **Then** chat messages are stored in the PostgreSQL database linked to the user session.
3. **Given** a request for past session data, **When** the data is retrieved, **Then** the correct session and chat history (if stored) are returned.

### Edge Cases

- What happens when Qdrant is unavailable during embedding or querying?
- How does the system handle very long book content chunks or queries?
- What are the rate limits for the embedding model API?
- How does the system handle concurrent requests to the API endpoints?
- What happens if the Neon PostgreSQL database connection fails?

## Requirements

### Functional Requirements

- **FR-001**: The system MUST create a new FastAPI project under a `backend/` folder.
- **FR-002**: The system MUST implement a `/embed` API endpoint to accept book content chunks, chunk them, generate embeddings, and store them in a Qdrant collection.
- **FR-003**: The system MUST implement a `/query` API endpoint to accept user questions, perform a vector search in Qdrant, and return relevant text chunks.
- **FR-004**: The system MUST implement a `/chat` API endpoint to accept user input, retrieve relevant context using the RAG pipeline, and return an assembled assistant response.
- **FR-005**: The system MUST enable CORS for frontend Docusaurus integration.
- **FR-006**: The system MUST set up a Qdrant collection specifically for book embeddings.
- **FR-007**: The system MUST implement functions to `upsert` and `search` embeddings in Qdrant.
- **FR-008**: The system MUST store Qdrant connection credentials in a `.env` file.
- **FR-009**: The system MUST create database tables in Neon PostgreSQL for user sessions and optional chat history.
- **FR-010**: The system MUST implement database helper functions for inserting and retrieving session data from Neon PostgreSQL.
- **FR-011**: The system MUST implement backend logic for text chunking of book content.
- **FR-012**: The system MUST implement backend logic for generating embeddings using OpenAI or Claude Code embeddings.
- **FR-013**: The system MUST implement backend logic for vector search in Qdrant.
- **FR-014**: The system MUST implement backend logic for assembling assistant responses for the chatbot.
- **FR-015**: The system MUST store all API keys, database URLs, and secrets in `.env` files.
- **FR-016**: The system MUST implement unit tests for the `/embed` endpoint to validate embeddings are stored correctly.
- **FR-017**: The system MUST implement unit tests for the `/query` endpoint to validate correct retrieval of text chunks.
- **FR-018**: The system MUST implement unit tests for the `/chat` endpoint to validate response assembly.
- **FR-019**: The system MUST simulate queries with dummy book content to ensure the backend works independently.

### Key Entities

-   **Book Content Chunk**: A segment of the book's text, used for embedding and retrieval.
    -   Attributes: `id`, `text`, `embedding` (vector), `metadata` (e.g., chapter, module, page).
-   **User Question**: Text input from the user to the chatbot.
-   **Chat Session**: A continuous interaction between a user and the chatbot.
    -   Attributes: `session_id`, `start_time`, `end_time`, `user_id` (if applicable).
-   **Chat Message**: A single message within a chat session, from either user or bot.
    -   Attributes: `message_id`, `session_id`, `sender` ('user' or 'bot'), `text`, `timestamp`.
-   **Embedding**: A numerical vector representation of text content.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: The `/embed` endpoint processes 100 book content chunks within 10 seconds with a success rate of 99%.
-   **SC-002**: The `/query` endpoint returns relevant text chunks for 90% of user questions within 1 second.
-   **SC-003**: The `/chat` endpoint provides an assembled assistant response within 3 seconds for 95% of user inputs.
-   **SC-004**: The RAG pipeline accurately retrieves context for 95% of relevant user questions, leading to factual answers.
-   **SC-005**: User session data is successfully stored and retrieved from the PostgreSQL database in less than 500ms.
-   **SC-006**: All unit tests for `/embed`, `/query`, and `/chat` endpoints pass with 100% success.
