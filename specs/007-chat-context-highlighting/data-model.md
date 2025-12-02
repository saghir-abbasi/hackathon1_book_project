# Data Model: Chat Search, Highlighting & Context Injection UI

**Feature Branch**: `007-chat-context-highlighting`  
**Date**: 2025-12-02
**Spec**: `specs/007-chat-context-highlighting/spec.md`
**Plan**: `specs/007-chat-context-highlighting/plan.md`
**Research**: `specs/007-chat-context-highlighting/research.md`

## Key Entities

### SelectedContext

Represents the user's selected text and its associated metadata, transmitted from the frontend to the backend. This data is used to provide contextual information to the RAG chatbot.

*   **Attributes**:
    *   `selectedText` (string): The exact text content selected by the user.
        *   **Validation Rule**: Max length 1000 characters. Must be sanitized (HTML stripped).
    *   `chapterId` (string, optional): The ID of the chapter where the text was selected (derived from `<h1>` tag's `id`).
        *   **Validation Rule**: Must be a valid string identifier.
    *   `sectionId` (string, optional): The ID of the section where the text was selected (derived from `<h2>`/`<h3>` tag's `id`).
        *   **Validation Rule**: Must be a valid string identifier.
    *   `offsets` (array of integers, optional): An array containing the start and end character offsets of the `selectedText` within its parent HTML element. Format: `[start_offset, end_offset]`.
        *   **Validation Rule**: Must be an array of two non-negative integers.

*   **Relationships**:
    *   Integrated into the `ChatRequest` payload sent to the backend.

*   **Purpose**: To provide explicit contextual information for RAG (Retrieval Augmented Generation) within the chatbot.
