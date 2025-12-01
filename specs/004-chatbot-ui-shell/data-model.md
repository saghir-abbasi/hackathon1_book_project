# Data Model: Chatbot Client-Side State

**Date**: 2025-12-01
**Feature**: [Chatbot UI Shell in Docusaurus](spec.md)

This document outlines the data structures used for managing the chatbot's state on the client-side. As this feature has no backend, all data is ephemeral and stored in React component state.

## Key Entities

### `Message`

Represents a single message in the chat history.

-   **`id`** (string, mandatory): A unique identifier for the message (e.g., generated with `Date.now()` or a UUID library).
-   **`text`** (string, mandatory): The content of the message.
-   **`sender`** (enum, mandatory): Indicates who sent the message.
    -   `'user'`: The message is from the end-user.
    -   `'bot'`: The message is from the AI assistant.
-   **`timestamp`** (Date, mandatory): The time when the message was created.

### Example `Message` Object:

```json
{
  "id": "1670000000000",
  "text": "Hello, what is a URDF file?",
  "sender": "user",
  "timestamp": "2025-12-01T10:00:00.000Z"
}
```

### `ChatState`

Represents the complete state of the chatbot widget at any given time.

-   **`isOpen`** (boolean): Tracks whether the chat window is visible.
-   **`messages`** (Array<`Message`>): An array of `Message` objects representing the conversation history.
-   **`isThinking`** (boolean): A flag to indicate if the bot is currently "thinking" (i.e., waiting to display a placeholder response).

### Example `ChatState` Object:

```json
{
  "isOpen": true,
  "messages": [
    {
      "id": "1670000000000",
      "text": "Hello, what is a URDF file?",
      "sender": "user",
      "timestamp": "2025-12-01T10:00:00.000Z"
    },
    {
      "id": "1670000001000",
      "text": "This is a placeholder response.",
      "sender": "bot",
      "timestamp": "2025-12-01T10:00:01.000Z"
    }
  ],
  "isThinking": false
}
```

## State Transitions

-   User clicks chatbot button: `isOpen` toggles `true`/`false`.
-   User sends a message: A new `Message` object with `sender: 'user'` is added to the `messages` array. `isThinking` is set to `true`.
-   Bot "replies": `isThinking` is set to `false`. A new `Message` object with `sender: 'bot'` is added to the `messages` array.
