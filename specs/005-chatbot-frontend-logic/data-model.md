# Data Model: Chatbot Zustand Store

**Date**: 2025-12-01
**Feature**: [Chatbot Frontend Logic & UX Enhancements](spec.md)

This document outlines the data structures for the chatbot's client-side state, which will be managed by a centralized Zustand store.

## Key Entities & State Structure

### `Message`

Represents a single message in the chat history. This structure is consistent with the feature specification.

-   **`id`** (string, mandatory): A unique identifier for the message.
-   **`role`** (enum, mandatory): Indicates the sender.
    -   `'user'`: The end-user.
    -   `'assistant'`: The AI assistant.
    -   `'system'`: An administrative or error message.
-   **`content`** (string, mandatory): The raw string content of the message, which may contain Markdown.
-   **`timestamp`** (Date, mandatory): The time when the message was created.

### `ChatState` (Zustand Store)

This defines the shape of the entire state managed by Zustand. It includes both the data and the actions that can be performed on it.

-   **`messages`** (Array<`Message`>): The ordered list of all messages in the current session.
-   **`isLoading`** (boolean): `true` when the assistant is preparing a mock response, used to show a typing indicator and disable the input.
-   **`error`** (string | null): Stores any mock error message to be displayed to the user.
-   **`contextMode`** (enum): The currently selected context for the chat.
    -   `'full_book'`
    -   `'selected_text'`

### `ChatActions` (Zustand Store)

These are the functions that will be part of the store to modify the state.

-   **`addMessage(message: Message)`**: Adds a new message to the `messages` array.
-   **`setLoading(isLoading: boolean)`**: Sets the loading state.
-   **`setError(error: string | null)`**: Sets or clears an error message.
-   **`setContextMode(mode: 'full_book' | 'selected_text')`**: Switches the context mode.
-   **`resetChat()`**: Clears the `messages` array and resets `error` and `isLoading` to their initial states.

### Example Zustand Store Shape:

```typescript
import { create } from 'zustand';

type Message = {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
};

type ContextMode = 'full_book' | 'selected_text';

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  contextMode: ContextMode;
  addMessage: (message: Message) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setContextMode: (mode: ContextMode) => void;
  resetChat: () => void;
}

const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,
  error: null,
  contextMode: 'full_book',
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  setContextMode: (mode) => set({ contextMode: mode }),
  resetChat: () => set({ messages: [], error: null, isLoading: false }),
}));
```
