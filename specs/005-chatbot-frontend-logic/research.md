# Research: Chatbot State Management and Markdown Rendering

**Date**: 2025-12-01
**Feature**: [Chatbot Frontend Logic & UX Enhancements](spec.md)

## Decision 1: Use Zustand for State Management

The chatbot's client-side state, which includes the message history, loading status, and context mode, will be managed using `Zustand`.

### Rationale

1.  **Simplicity and Minimal Boilerplate**: Zustand offers a simple, un-opinionated API that is easy to adopt. It avoids the extensive boilerplate associated with libraries like Redux, making the codebase cleaner and more maintainable.
2.  **Centralized Store**: It provides a centralized store that can be accessed from any component in the tree without "prop drilling" (passing props down through multiple layers). This is a significant advantage over using `useState` and `useContext` as the component tree grows.
3.  **Performance**: Zustand is designed to be performant. Components subscribe only to the state slices they need, which prevents unnecessary re-renders.
4.  **Scalability**: While lightweight, Zustand is scalable enough to handle the future complexity of the chatbot without requiring a migration to a heavier library later on.

### Alternatives Considered

-   **React `useState` + `useContext`**:
    -   **Reason for Rejection**: This approach becomes cumbersome as more state needs to be shared across different components. It often leads to "prop drilling" and can cause performance issues due to components re-rendering even if the state they depend on hasn't changed. Given the number of interacting components in this feature (Input, MessageList, ContextSelector), a dedicated store is more efficient.

## Decision 2: Use `react-markdown` and `remark-gfm` for Rendering

Message content will be rendered using the `react-markdown` library, with the `remark-gfm` plugin to support GitHub Flavored Markdown (tables, strikethrough, etc.). Syntax highlighting for code blocks will be handled by `react-syntax-highlighter`.

### Rationale

1.  **Spec Compliance**: The feature specification explicitly requires Markdown rendering capabilities.
2.  **Robust and Secure**: `react-markdown` is a widely-used and well-maintained library that safely parses and renders Markdown content in React, preventing XSS attacks by default.
3.  **Extensible**: It is highly extensible with a rich ecosystem of plugins (`remark` and `rehype` plugins). `remark-gfm` is essential for a good user experience with technical content, and `react-syntax-highlighter` is the standard for code block styling.

### Alternatives Considered

-   **`marked` or other libraries**:
    -   **Reason for Rejection**: While other libraries exist, `react-markdown` is specifically designed for React and integrates seamlessly into the component lifecycle, making it the most idiomatic choice for this project.
