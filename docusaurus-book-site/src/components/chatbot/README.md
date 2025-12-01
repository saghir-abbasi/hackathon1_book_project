# Chatbot Component

This directory contains the Docusaurus Chatbot component, providing a floating button and an interactive chat window.

## Component Hierarchy:

-   `index.tsx`: The main container component that manages the chatbot's open/close state, message history, and bot "thinking" state. It renders `ChatbotButton` and `ChatWindow`.
-   `ChatbotButton.tsx`: The floating button that toggles the visibility of the `ChatWindow`.
-   `ChatWindow.tsx`: The main chat interface, containing the header, message display area, and `ChatInput`. It maps over the `messages` state to render `ChatMessage` components.
-   `components/ChatMessage.tsx`: Displays a single chat message, differentiating between user and bot messages.
-   `components/ChatInput.tsx`: The input field and send button for users to type and send messages.
-   `chatbot.module.css`: Contains all the styles for the chatbot components, including the robotics theme and responsive adjustments.

## State Management:

The chatbot uses React's `useState` hook for local state management within `index.tsx`:

-   `isOpen`: Boolean, controls the visibility of the chat window.
-   `messages`: Array of `Message` objects, storing the conversation history. Each `Message` object has an `id`, `text`, `sender` ('user' or 'bot'), and `timestamp`.
-   `isThinking`: Boolean, indicates when the bot is simulating a response.

The `handleSendMessage` function in `index.tsx` is responsible for adding user messages to the history and triggering a simulated bot reply using `setTimeout`.

## Customization:

### Theming:

The visual theme is defined in `chatbot.module.css` using CSS custom properties (variables) prefixed with `--chatbot-`. These can be easily modified to change colors, fonts, and other stylistic elements to match different themes.

### Simulated Bot Responses:

The current bot responses are simulated using a `setTimeout` function in `index.tsx`. This is a placeholder for future backend integration. To integrate with a real API, replace the `setTimeout` logic within `handleSendMessage` with an actual API call (e.g., using `fetch` or `axios`).

## Global Availability:

The `Chatbot` component is integrated globally into the Docusaurus site by rendering it within `docusaurus-book-site/src/theme/Root.tsx`. This ensures the chatbot button is present on all pages.

## Development Notes:

-   **Responsiveness**: Styles include media queries for optimal display on mobile and tablet devices.
-   **Animations**: CSS transitions and keyframe animations are used for smooth UI interactions (e.g., chat window open/close, message fade-in).
-   **No External UI Libraries**: The component is built using plain React, CSS Modules, and native browser APIs to keep the bundle size small and avoid unnecessary dependencies.