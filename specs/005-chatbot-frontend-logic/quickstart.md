# Quickstart: Running the Enhanced Chatbot UI

**Date**: 2025-12-01
**Feature**: [Chatbot Frontend Logic & UX Enhancements](spec.md)

This guide provides the steps to install new dependencies, run the Docusaurus site, and test the enhanced chatbot UI.

## Prerequisites

-   Node.js (LTS version recommended)
-   npm or yarn installed

## Running the Development Server

1.  **Navigate to the Docusaurus directory**:
    ```bash
    cd docusaurus-book-site
    ```

2.  **Install new dependencies**:
    This feature requires new libraries for state management and Markdown rendering.
    ```bash
    npm install zustand react-markdown remark-gfm react-syntax-highlighter
    ```
    or
    ```bash
    yarn add zustand react-markdown remark-gfm react-syntax-highlighter
    ```

3.  **Start the development server**:
    ```bash
    npm run start
    ```
    or
    ```bash
    yarn start
    ```

4.  **View the site**:
    Open your web browser and go to `http://localhost:3000`.

## How to Verify

-   Open the chatbot and verify the new robotics-themed UI.
-   Send a message containing Markdown (e.g., `` `code` ``, `**bold**`) and confirm it renders correctly.
-   Verify that a "typing" indicator appears while the mock assistant is replying.
-   Check that the input field is disabled during the mock reply.
-   Use `Shift+Enter` to create a new line in the input.
-   Find and test the "Reset Chat" button.
-   Find and test the "Context Mode" selector.
