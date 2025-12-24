# Data Model: Personalization & Translation UI

**Feature**: 008-feature-personalization-translation
**Date**: 2025-12-22

## Entities

### 1. UserPreferences (Client-side localStorage)

Stores user's background preference for content personalization.

```typescript
interface UserPreferences {
  /**
   * User's professional background for content personalization.
   * - 'software': Emphasize code, APIs, software patterns
   * - 'hardware': Emphasize circuits, sensors, electronics
   * - null: Not yet selected
   */
  background: 'software' | 'hardware' | null;

  /**
   * ISO 8601 timestamp of when preference was last updated.
   * Used for cache invalidation if needed.
   */
  lastUpdated: string;
}
```

**Storage Key**: `book_user_preferences`

**Validation Rules**:
- `background` must be one of: `'software'`, `'hardware'`, or `null`
- `lastUpdated` must be a valid ISO 8601 date string

### 2. ContentTransformRequest

Request payload sent to Agent API for content transformation.

```typescript
interface ContentTransformRequest {
  /**
   * The user's query/instruction for the agent.
   * For personalization: "Personalize this content for a {background} background"
   * For translation: "Translate this content to Urdu"
   */
  userQuery: string;

  /**
   * The chapter ID from which content is being transformed.
   * Used for context and logging.
   */
  chapterId: string;

  /**
   * Session identifier for the transformation request.
   * Generated per-transformation or reused from chatbot.
   */
  sessionId: string;

  /**
   * User identifier (can be 'anonymous' for non-authenticated users).
   */
  userId: string;

  /**
   * The full chapter content to be transformed.
   * Extracted from the current page's main content area.
   */
  selectedText: string;
}
```

### 3. TransformationState

React state for managing the transformation UI.

```typescript
interface TransformationState {
  /**
   * Current status of the transformation process.
   */
  status: 'idle' | 'loading' | 'streaming' | 'complete' | 'error';

  /**
   * Type of transformation being performed.
   */
  type: 'personalize' | 'translate' | null;

  /**
   * Accumulated transformed content from streaming response.
   */
  content: string;

  /**
   * Error message if transformation failed.
   */
  error: string | null;

  /**
   * Whether to show the content overlay.
   */
  showOverlay: boolean;
}
```

**State Transitions**:
```
idle → loading (user clicks button)
loading → streaming (first chunk received)
streaming → streaming (more chunks)
streaming → complete (stream ends)
loading/streaming → error (error occurs)
complete/error → idle (user closes overlay)
```

### 4. ChapterMetadata

Metadata extracted from current chapter for transformation context.

```typescript
interface ChapterMetadata {
  /**
   * Unique identifier for the chapter (from URL or frontmatter).
   */
  id: string;

  /**
   * Chapter title for display purposes.
   */
  title: string;

  /**
   * Full text content of the chapter (HTML stripped).
   */
  textContent: string;

  /**
   * Module the chapter belongs to.
   */
  module: string;
}
```

## localStorage Schema

```json
{
  "book_user_preferences": {
    "background": "software",
    "lastUpdated": "2025-12-22T10:30:00.000Z"
  }
}
```

## State Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User on Chapter Page                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  ChapterToolbar renders with Personalize & Translate buttons │
│  useUserPreferences() loads background from localStorage     │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│ Click "Personalize"   │           │ Click "Translate"     │
└───────────────────────┘           └───────────────────────┘
            │                                   │
            ▼                                   │
┌───────────────────────┐                       │
│ background === null?  │                       │
│   YES → Show Modal    │                       │
│   NO → Continue       │                       │
└───────────────────────┘                       │
            │                                   │
            ▼                                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Extract chapter content (textContent)           │
│              Build ContentTransformRequest                   │
│              Call AgentBridge.sendChatMessage()              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Stream response via SSE                         │
│              Update TransformationState.content              │
│              Display in ContentOverlay                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              User views transformed content                  │
│              Can close overlay to return to original         │
└─────────────────────────────────────────────────────────────┘
```

## Relationships

```
UserPreferences (localStorage)
       │
       │ read by
       ▼
ChapterToolbar (React Component)
       │
       │ uses
       ├──────────────────────────────┐
       ▼                              ▼
PersonalizeButton              TranslateButton
       │                              │
       │ triggers                     │ triggers
       ▼                              ▼
ContentTransformRequest ◄─────────────┘
       │
       │ sent to
       ▼
AgentBridge → Backend API
       │
       │ streams
       ▼
TransformationState
       │
       │ displayed in
       ▼
ContentOverlay
```
