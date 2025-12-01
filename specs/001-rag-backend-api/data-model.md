# Data Model: Backend API Layer (FastAPI + Qdrant + Neon)

**Date**: 2025-12-01
**Feature**: [Backend API Layer (FastAPI + Qdrant + Neon)](../spec.md)

This document outlines the data models for the backend API layer, covering entities stored in Qdrant (vector database) and Neon Serverless PostgreSQL (relational database).

## Key Entities & Their Storage Locations

### `BookContentChunk` (Stored in Qdrant)

Represents a segment of the book's text suitable for embedding and retrieval.

-   **`id`** (string, unique): A unique identifier for the content chunk.
-   **`text`** (string): The actual text content of the chunk.
-   **`embedding`** (vector, float array): The high-dimensional vector representation of the `text`.
-   **`metadata`** (JSON object): Additional structured information about the chunk.
    -   `chapter` (string): The chapter the chunk belongs to.
    -   `module` (string): The module the chunk belongs to.
    -   `page` (number, optional): The page number within the book.
    -   `source_file` (string, optional): The original file path of the content.

### `UserSession` (Stored in Neon PostgreSQL)

Represents a continuous interaction session between a user and the chatbot.

-   **`session_id`** (UUID, primary key): Unique identifier for the session.
-   **`start_time`** (timestamp): The time when the session began.
-   **`last_active_time`** (timestamp): The last time there was activity in the session.
-   **`user_id`** (string, optional, foreign key to User table if authentication is added later): Identifier for the user, if available.
-   **`metadata`** (JSON object, optional): Arbitrary additional session-related data.

### `ChatMessage` (Stored in Neon PostgreSQL - optional, for chat history)

Represents a single message exchanged within a `UserSession`.

-   **`message_id`** (UUID, primary key): Unique identifier for the message.
-   **`session_id`** (UUID, foreign key to `UserSession.session_id`): Links the message to its session.
-   **`sender`** (enum, 'user' or 'bot'): Indicates who sent the message.
-   **`text`** (string): The content of the message.
-   **`timestamp`** (timestamp): The time when the message was sent.
-   **`context_retrieved`** (JSON object, optional): Metadata about the context retrieved for this message (e.g., Qdrant search results).

### `Embedding` (Conceptual, represents the vector generated)

A numerical vector representation of text content. This is a property of `BookContentChunk` and `UserQuestion` (when converted for search), not a standalone stored entity.

-   **`vector`** (float array): The actual high-dimensional vector.
-   **`model_id`** (string): Identifier for the embedding model used (e.g., 'text-embedding-ada-002', 'claude-3-haiku').

## Relationships

-   `UserSession` 1:N `ChatMessage`: One session can have multiple chat messages.
-   `BookContentChunk` has `Embedding`: An embedding is generated for each content chunk.

## API Request/Response Data Structures (Conceptual)

These will be formalized in the OpenAPI specification, but conceptually include:

### `/embed` Endpoint

-   **Request Body**:
    -   `content_chunks` (array of objects):
        -   `text` (string): Raw text to embed.
        -   `metadata` (JSON object, optional): Metadata for the chunk.
-   **Response Body**:
    -   `status` (string): "success" or "failure".
    -   `embedded_count` (number): Number of chunks successfully embedded.

### `/query` Endpoint

-   **Request Body**:
    -   `question` (string): User's question for vector search.
    -   `limit` (number, optional): Maximum number of results to return.
-   **Response Body**:
    -   `results` (array of objects):
        -   `text` (string): Retrieved text chunk.
        -   `metadata` (JSON object): Original metadata of the chunk.
        -   `score` (number): Relevance score from vector search.

### `/chat` Endpoint

-   **Request Body**:
    -   `session_id` (UUID, optional): Existing session ID. If not provided, a new one is created.
    -   `user_message` (string): The user's message.
    -   `chat_history` (array of `ChatMessage`, optional): Previous messages in the conversation.
-   **Response Body**:
    -   `session_id` (UUID): The current session ID.
    -   `assistant_response` (string): The chatbot's generated response.
    -   `chat_message_id` (UUID): ID of the new assistant message.
    -   `context_used` (array of strings, optional): Snippets of book content used to form the response.
