# Quickstart Guide: Feature 2.4 — OpenAI Agents / ChatKit Integration

This guide provides high-level steps to set up and run the AI Assistant feature.

## Prerequisites

-   Ensure the existing FastAPI backend (Feature 2.3) is set up and running.
-   Ensure the Docusaurus frontend is set up and running.
-   Access to OpenAI API keys or similar ChatKit service credentials.

## Backend Setup (AI Assistant Service)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment and install dependencies (if not already done for Feature 2.3):**
    ```bash
    python -m venv .venv
    ./.venv/Scripts/activate # On Windows
    source ./.venv/bin/activate # On macOS/Linux
    pip install -r requirements.txt
    ```
    *(Note: New dependencies for the AI Assistant will need to be added to `requirements.txt` and installed.)*

3.  **Configure API Keys:**
    -   Create or update the `.env` file in the `backend/` directory.
    -   Add your OpenAI API key or other necessary service credentials:
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        # Add other relevant API keys (e.g., QDRANT_API_KEY, NEON_DB_CONNECTION_STRING)
        ```
    -   *(Ensure these keys are kept secret and never committed to version control.)*

4.  **Run the FastAPI Backend:**
    ```bash
    uvicorn src.main:app --reload --port 8000
    ```
    *(The backend should now expose the new `/agent/stream` endpoint.)*

## Frontend Setup (Docusaurus Integration)

1.  **Navigate to the Docusaurus project directory:**
    ```bash
    cd docusaurus-book-site
    ```

2.  **Install dependencies (if new frontend dependencies are added):**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Ensure the new chat client plugin/component is integrated:**
    -   Verify that `plugins/local-chat-plugin/chatClient.js` (or similar path) exists and is correctly referenced in `docusaurus.config.ts`.
    -   Ensure the `ChatUIExtension.js` component is correctly integrated into the existing chat UI.

4.  **Run the Docusaurus Frontend:**
    ```bash
    npm start
    # or yarn start
    ```

## Interacting with the AI Assistant

-   Once both backend and frontend services are running, navigate to your Docusaurus site in a web browser.
-   Locate the chat interface (existing chat UI, now extended).
-   Type your queries into the chat window and observe streamed responses from the AI Assistant.
-   Test functionality like selected text context and chapter ID injection.

## Post-Setup Verification

-   Check backend logs for any errors related to agent initialization, tool calls, or streaming.
-   Monitor frontend console for any JavaScript errors from the chat client.
-   Verify that API keys are not exposed in the frontend network requests.
