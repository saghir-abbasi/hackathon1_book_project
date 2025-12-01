# Quickstart: RAG Chatbot Backend API

**Date**: 2025-12-01
**Feature**: [Backend API Layer (FastAPI + Qdrant + Neon)](../spec.md)

This guide provides instructions to set up and run the RAG Chatbot Backend API locally.

## Prerequisites

-   Python 3.9+
-   `pip` (Python package installer)
-   Docker (for running Qdrant locally, or access to a hosted Qdrant instance)
-   Access to a Neon Serverless PostgreSQL database or a local PostgreSQL instance.

## Setup Instructions

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd book_ai_robotics
    ```

2.  **Navigate to the backend directory**:
    ```bash
    cd backend/
    ```

3.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` will be created during implementation, containing FastAPI, Uvicorn, Qdrant Client, Psycopg2-binary, SQLAlchemy, Pydantic, python-dotenv, and an OpenAI/Claude API client.)*

5.  **Set up environment variables**:
    Create a `.env` file in the `backend/` directory based on `.env.example`.
    ```
    # Qdrant configuration
    QDRANT_HOST=<your_qdrant_host> # e.g., localhost:6333 for local Docker
    QDRANT_API_KEY=<your_qdrant_api_key> # Optional, if Qdrant requires authentication
    QDRANT_COLLECTION_NAME=book_embeddings

    # Neon PostgreSQL configuration
    DATABASE_URL="postgresql+psycopg2://user:password@host:port/database" # Your Neon DB URL
    # Example: postgresql+psycopg2://neon_user:neon_password@ep-random-name-12345.us-east-2.aws.neon.tech/neondb

    # Embedding Model Configuration
    EMBEDDING_MODEL_PROVIDER=openai # or 'claude'
    OPENAI_API_KEY=<your_openai_api_key> # Required if using OpenAI
    CLAUDE_API_KEY=<your_claude_api_key> # Required if using Claude

    # CORS settings (for Docusaurus frontend)
    CORS_ORIGINS=["http://localhost:3000"] # Adjust as needed
    ```

6.  **Run Qdrant locally (using Docker)**:
    If you don't have a hosted Qdrant instance, run it with Docker:
    ```bash
    docker run -p 6333:6333 -p 6334:6334 \
        -v $(pwd)/qdrant_data:/qdrant/data \
        qdrant/qdrant
    ```

7.  **Run the FastAPI application**:
    ```bash
    uvicorn src.api.main:app --host 0.0.0.0 --port 8000
    ```
    *(Note: `src.api.main:app` assumes the main FastAPI application instance is named `app` within `src/api/main.py`.)*

## API Endpoints

Once running, you can access the API at `http://localhost:8000`.
-   **`/docs`**: OpenAPI (Swagger UI) documentation for testing endpoints.
-   **`/redoc`**: ReDoc documentation.

## Verification

-   Use the `/docs` interface to test the `/embed`, `/query`, and `/chat` endpoints.
-   Monitor Qdrant for new embeddings after calling `/embed`.
-   Monitor Neon PostgreSQL for new user sessions and chat messages after calling `/chat`.
