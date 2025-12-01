# Chatbot UI Component

This directory contains the front-end UI shell for the AI Assistant chatbot, designed for integration into the Docusaurus book site. This component provides the visual interface and basic interaction logic without any backend connectivity.

## Component Hierarchy

-   **`index.tsx` (Chatbot Container)**: The main entry point. Manages the overall state (`isOpen`, `messages`, `isThinking`), renders `ChatbotButton` and `ChatWindow`.
-   **`ChatbotButton.tsx`**: The floating button component that toggles the `ChatWindow` visibility.
-   **`ChatWindow.tsx`**: The main panel for the chat interface. Contains the header, message list, and input area.
-   **`components/`**:
    -   **`ChatMessage.tsx`**: Displays a single chat message (user or bot).
    -   **`ChatInput.tsx`**: Provides the text input field and send button.

## State Management

The chatbot's state is managed locally within the `index.tsx` (Chatbot Container) using React's `useState` hook. Key state variables include:

-   `isOpen`: Boolean, controls the visibility of the `ChatWindow`.
-   `messages`: Array of `Message` objects, stores the conversation history.
-   `isThinking`: Boolean, indicates when the bot is simulating a response.

The `Message` data structure is defined as:
`{ id: string; text: string; sender: 'user' | 'bot'; timestamp: Date; }`

## Theme Customization

The visual theme is applied using CSS Modules (`chatbot.module.css`). All major styling variables (colors, fonts, borders) are defined at the top of this file using CSS custom properties (`--neon-cyan`, `--electric-blue`, etc.).

To customize the theme:
1.  Modify the CSS variable values in `docusaurus-book-site/src/components/chatbot/chatbot.module.css`.
2.  Adjust styles for individual components within the same CSS module.

## Docusaurus Integration

The chatbot is integrated globally into the Docusaurus site via the `docusaurus-book-site/src/theme/Root.tsx` file. The `Chatbot` component from `index.tsx` is rendered as a child of the `Root` component, ensuring its presence on all pages.

## Extending for Backend API Integration

Currently, bot responses are simulated using a `setTimeout` function in `index.tsx` (`handleSendMessage` function).

**To integrate a backend API (e.g., in Feature 2.6):**

1.  Locate the `handleSendMessage` function in `docusaurus-book-site/src/components/chatbot/index.tsx`.
2.  Replace the `setTimeout` block that generates the placeholder bot response with an actual HTTP API call (e.g., using `fetch` or `axios`) to your backend endpoint.
3.  Handle the API response: parse the actual bot message and update the `messages` state accordingly.
4.  Ensure error handling is in place for API failures.
5.  Consider moving the API call logic to a separate service file or custom hook for better separation of concerns.
