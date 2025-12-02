# Quickstart Guide: Chat Search, Highlighting & Context Injection UI

**Feature Branch**: `007-chat-context-highlighting`  
**Date**: 2025-12-02
**Spec**: `specs/007-chat-context-highlighting/spec.md`
**Plan**: `specs/007-chat-context-highlighting/plan.md`
**Research**: `specs/007-chat-context-highlighting/research.md`

## Overview

This guide provides high-level instructions to set up and test the "Chat Search, Highlighting & Context Injection UI" feature. This feature allows users to select text in the Docusaurus book, triggering a contextual query to the RAG chatbot.

## Setup Steps (Local Development)

### 1. Checkout Feature Branch

Ensure you are on the correct feature branch:

```bash
git checkout 007-chat-context-highlighting
```

### 2. Frontend Setup (Docusaurus)

Navigate to the Docusaurus project directory and install dependencies:

```bash
cd docusaurus-book-site
npm install
```

Start the Docusaurus development server:

```bash
npm start
```

### 3. Backend Setup

Navigate to the backend project directory and set up the Python virtual environment and dependencies:

```bash
cd backend
python -m venv .venv
./.venv/Scripts/activate # On Windows
# source .venv/bin/activate # On Linux/macOS
pip install -r requirements.txt
```

Start the FastAPI backend server:

```bash
# Assuming main.py is the entry point
python src/main.py
```

### 4. Agent Setup

Ensure your AI agent (e.g., Gemini or OpenAI) is properly configured with the necessary API keys and access. The backend will communicate with this agent.

## Testing the Feature

### 1. Activate Text Selection

1.  Open your Docusaurus site in a web browser (`http://localhost:3000` by default).
2.  Navigate to any documentation page.
3.  Select a passage of text on the page with your mouse or keyboard.

### 2. Verify "Ask About This" Button

1.  After selecting text, observe that a floating "Ask About This" button appears near your selection.

### 3. Initiate Contextual Query

1.  Click the "Ask About This" button.
2.  The chatbot panel should open (if not already open).
3.  Verify that the selected text appears as a "Context Bubble" above the chat input box.

### 4. Ask a Question

1.  Type a question related to the selected text into the chat input box.
2.  Submit the question.
3.  Verify that the chatbot's response is relevant and specifically grounded in the context of the text you selected.

### 5. Remove Context

1.  Locate the "remove" or "X" button on the context bubble in the chat panel.
2.  Click the button.
3.  Verify that the context bubble disappears, and subsequent queries are no longer constrained by the previous selection.

## Troubleshooting

*   If the "Ask About This" button doesn't appear, check browser console for JavaScript errors related to `useTextSelection.js`.
*   If the chatbot doesn't open or respond, check network requests in browser dev tools for errors when communicating with the backend (`POST /chat`).
*   Ensure both frontend and backend development servers are running.
*   Verify API keys and environment variables are correctly set for the backend and agent.
