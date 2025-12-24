# API Contract: Personalization & Translation

**Feature**: 008-feature-personalization-translation
**Date**: 2025-12-22

## Overview

This feature reuses the existing Agent API endpoint (`/api/agent/query`) for content transformation. No new backend endpoints are required. The transformation is achieved through carefully crafted prompts.

## Existing Endpoint: POST /api/agent/query

### Request

```typescript
interface AgentQueryRequest {
  userQuery: string;      // The transformation instruction
  chapterId: string;      // Current chapter ID
  sessionId: string;      // Session identifier
  userId: string;         // User identifier (can be 'anonymous')
  selectedText?: string;  // Chapter content to transform
  lastModelMessages?: Array<{role: string; content: string}>;
}
```

### Response

Server-Sent Events (SSE) stream:

```
data: {"token": "Based"}

data: {"token": " on"}

data: {"token": " your"}

...

data: {"event": "end", "token": ""}

```

### Content-Type

```
text/event-stream
```

## Transformation Prompts

### Personalization - Software Background

```typescript
const PERSONALIZE_SOFTWARE_PROMPT = `
You are adapting robotics educational content for a SOFTWARE DEVELOPER audience.

INSTRUCTIONS:
1. Rewrite the content emphasizing software concepts: code patterns, APIs, data structures, algorithms
2. Use analogies from: web development, databases, microservices, cloud computing, DevOps
3. When discussing hardware concepts, explain them in terms a software developer would understand
4. Keep all technical accuracy - just change the framing and examples
5. Maintain the same structure and section headings
6. Output in Markdown format

ORIGINAL CONTENT:
{chapterContent}

PERSONALIZED CONTENT FOR SOFTWARE DEVELOPERS:
`;
```

### Personalization - Hardware Background

```typescript
const PERSONALIZE_HARDWARE_PROMPT = `
You are adapting robotics educational content for a HARDWARE ENGINEER audience.

INSTRUCTIONS:
1. Rewrite the content emphasizing hardware concepts: circuits, sensors, actuators, power systems
2. Use analogies from: electronics, embedded systems, control theory, mechanical engineering
3. When discussing software concepts, explain them in terms a hardware engineer would understand
4. Keep all technical accuracy - just change the framing and examples
5. Maintain the same structure and section headings
6. Output in Markdown format

ORIGINAL CONTENT:
{chapterContent}

PERSONALIZED CONTENT FOR HARDWARE ENGINEERS:
`;
```

### Translation to Urdu

```typescript
const TRANSLATE_URDU_PROMPT = `
Translate the following robotics educational content to Urdu.

INSTRUCTIONS:
1. Translate all explanatory text to Urdu
2. Keep technical terms in English where no standard Urdu equivalent exists (e.g., "ROS 2", "node", "topic")
3. For code blocks, keep the code in English but translate comments to Urdu
4. Maintain the same Markdown structure
5. Ensure the translation is clear, educational, and readable
6. Use formal Urdu appropriate for technical education

ORIGINAL CONTENT:
{chapterContent}

URDU TRANSLATION:
`;
```

## Request Examples

### Personalization Request (Software)

```json
{
  "userQuery": "You are adapting robotics educational content for a SOFTWARE DEVELOPER audience...",
  "chapterId": "chapter-1-ros2-basics",
  "sessionId": "transform-1703234567890",
  "userId": "anonymous",
  "selectedText": "# Introduction to ROS 2 Nodes and Topics\n\n## Introduction\n\nThis chapter introduces..."
}
```

### Translation Request (Urdu)

```json
{
  "userQuery": "Translate the following robotics educational content to Urdu...",
  "chapterId": "chapter-1-ros2-basics",
  "sessionId": "translate-1703234567890",
  "userId": "anonymous",
  "selectedText": "# Introduction to ROS 2 Nodes and Topics\n\n## Introduction\n\nThis chapter introduces..."
}
```

## Error Handling

### Error Response (SSE)

```
data: {"error": "Error message", "event": "error"}

```

### Client-Side Handling

```typescript
agentBridge.setCallbacks({
  onToken: (token: string) => {
    // Append token to transformed content
    setTransformedContent(prev => prev + token);
  },
  onComplete: () => {
    // Mark transformation as complete
    setStatus('complete');
  },
  onError: (error: Error) => {
    // Show error message to user
    setError(error.message);
    setStatus('error');
  }
});
```

## Rate Limiting

The existing Agent API rate limiting applies:
- Requests per session: Subject to backend configuration
- Content length: Existing `selectedText` size caps apply

## Content Extraction

The frontend must extract clean text content from the chapter:

```typescript
function extractChapterContent(): string {
  // Select main content area (Docusaurus-specific selector)
  const contentElement = document.querySelector('.theme-doc-markdown');

  if (!contentElement) {
    throw new Error('Could not find chapter content');
  }

  // Get text content, preserving some structure
  return contentElement.innerText;
}
```

## Sequence Diagram

```
┌──────────┐          ┌───────────────┐          ┌─────────────┐
│  User    │          │   Frontend    │          │   Backend   │
└────┬─────┘          └───────┬───────┘          └──────┬──────┘
     │                        │                         │
     │ Click "Personalize"    │                         │
     │───────────────────────>│                         │
     │                        │                         │
     │                        │ Extract chapter content │
     │                        │──────────┐              │
     │                        │          │              │
     │                        │<─────────┘              │
     │                        │                         │
     │                        │ POST /api/agent/query   │
     │                        │────────────────────────>│
     │                        │                         │
     │                        │    SSE: token stream    │
     │                        │<────────────────────────│
     │                        │                         │
     │ Display streaming      │                         │
     │<───────────────────────│                         │
     │                        │                         │
     │                        │    SSE: end event       │
     │                        │<────────────────────────│
     │                        │                         │
     │ Show complete content  │                         │
     │<───────────────────────│                         │
     │                        │                         │
```
