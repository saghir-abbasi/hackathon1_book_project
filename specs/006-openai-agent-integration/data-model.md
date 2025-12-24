# Data Model for Feature 2.4 — OpenAI Agents / ChatKit Integration

## Entities

### User

Represents an individual interacting with the system.

-   **id**: Unique identifier for the user.
-   **session_token**: Token for authenticating and identifying user sessions.

### Chat Session

Represents a continuous conversation between a user and the AI Assistant.

-   **session_id**: Unique identifier for the chat session.
-   **user_id**: Reference to the User entity.
-   **message_history**: Ordered list of messages exchanged within the session, maintaining conversational context.
-   **start_time**: Timestamp of session initiation.
-   **last_activity_time**: Timestamp of the last user interaction.
-   **chapter_context**: Identifier of the book chapter the user is currently viewing or has provided.

### AI Assistant Query Input

Data structure representing a user's request to the AI Assistant.

-   **user_query**: The natural language question or prompt from the user.
-   **selected_text**: Optional text segment highlighted by the user from the frontend, providing additional context.
-   **chapter_id**: Identifier of the book chapter from which the query originated or to which the selected text belongs.
-   **session_id**: Identifier of the current chat session.
-   **last_model_messages**: The last few messages from the AI assistant in the current session, for context.

### AI Assistant Response Output

Data structure representing the AI Assistant's streamed response.

-   **token**: A piece of the streamed response (word, sentence fragment).
-   **is_final**: Boolean indicating if this is the last token in the response.
-   **session_id**: Identifier of the chat session this response belongs to.
-   **tool_calls**: Optional, structured data indicating if the AI assistant invoked any tools.

### RAG Retrieval Result

Data structure representing relevant information retrieved by the RAG tool.

-   **segment_id**: Unique identifier for the retrieved text segment.
-   **content**: The textual content of the retrieved segment.
-   **source_chapter_id**: The chapter ID from which the segment was retrieved.
-   **relevance_score**: A score indicating how relevant the segment is to the query.

## Relationships

-   **User has many Chat Sessions**: One user can engage in multiple chat sessions.
-   **Chat Session contains many AI Assistant Query Inputs and Response Outputs**: Each query and response token belongs to a specific chat session.
-   **AI Assistant utilizes RAG Retrieval Results**: The AI Assistant's reasoning process incorporates data from RAG retrieval.
