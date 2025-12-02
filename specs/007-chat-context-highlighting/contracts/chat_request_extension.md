# API Contract: Chat Request Extension for Context Injection

**Feature Branch**: `007-chat-context-highlighting`  
**Date**: 2025-12-02
**Spec**: `specs/007-chat-context-highlighting/spec.md`
**Plan**: `specs/007-chat-context-highlighting/plan.md`
**Research**: `specs/007-chat-context-highlighting/research.md`
**Data Model**: `specs/007-chat-context-highlighting/data-model.md`

## Endpoint Modification

### `POST /chat`

This existing endpoint's request payload will be extended additively to include contextual information from user selections in the frontend.

#### Request Body (Modified `ChatRequest` Pydantic Model)

The `ChatRequest` model defined in `backend/src/models/chat_models.py` will be updated to include the following optional fields:

```python
from typing import List, Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_query: str
    session_id: str
    user_id: str
    # ... (other existing fields) ...

    # New fields for contextual queries
    selected_text: Optional[str] = None
    chapter_id: Optional[str] = None
    section_id: Optional[str] = None
    offsets: Optional[List[int]] = None
```

*   **`selected_text`**:
    *   **Type**: `string`
    *   **Description**: The text content selected by the user in the Docusaurus book.
    *   **Constraints**: Max length 1000 characters. Sanitized (HTML stripped).
    *   **Example**: `"This is an important paragraph about robotics."`

*   **`chapter_id`**:
    *   **Type**: `string`
    *   **Description**: The ID of the Docusaurus chapter (e.g., from an `<h1>` tag's `id`) where the text was selected.
    *   **Constraints**: Optional.
    *   **Example**: `"module-1-introduction"`

*   **`section_id`**:
    *   **Type**: `string`
    *   **Description**: The ID of the Docusaurus section (e.g., from an `<h2>` or `<h3>` tag's `id`) where the text was selected.
    *   **Constraints**: Optional.
    *   **Example**: `"robot-anatomy"`

*   **`offsets`**:
    *   **Type**: `array` of `integer`
    *   **Description**: Character offsets `[start, end]` of the `selected_text` within its containing HTML element on the page.
    *   **Constraints**: Optional. Array must contain two non-negative integers.
    *   **Example**: `[120, 250]`

#### Response Body

The response body (streamed response) remains unchanged as per the safety requirements and `Frontend–Backend Streaming Integrity` functional requirement (FR-008 in the spec). The new metadata is additive to the request, not affecting the response format.
