# RAG Chatbot Backend API

This project implements the backend services for a Retrieval-Augmented Generation (RAG) chatbot, designed to interact with book content. It uses FastAPI for the API, Qdrant as a vector database for embeddings, and Neon Serverless PostgreSQL for managing chat sessions and history.

## Features

- **Book Content Embedding**: Accepts book content chunks, generates embeddings, and stores them in Qdrant.
- **Vector Search**: Retrieves relevant book content segments from Qdrant based on user questions.
- **Chatbot Interaction**: Provides RAG-powered responses to user queries, leveraging retrieved context and LLM inference.
- **Session Management**: Stores and manages chat sessions and history in Neon PostgreSQL.
- **Isolated Development**: All backend components are developed within this `backend/` directory, ensuring no interference with existing frontend projects or other parts of the repository.

## Getting Started

Follow the instructions in `quickstart.md` (located in `specs/001-rag-backend-api/`) to set up and run the backend API locally.

## Project Structure

```
backend/
├── src/
│   ├── api/                 # FastAPI application and endpoints
│   ├── core/                # Core logic: RAG pipeline, chunking, embeddings
│   ├── db/                  # Database interaction (Qdrant, PostgreSQL)
│   ├── models/              # Pydantic models for request/response, DB schemas
│   └── services/            # Business logic and external service integrations
├── tests/                   # Unit and integration tests
├── .env.example             # Example environment variables
├── Dockerfile               # Dockerfile for containerization
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## API Endpoints

The API exposes the following endpoints (details in `specs/001-rag-backend-api/contracts/openapi.yaml`):

-   `POST /embed`: To embed book content chunks.
-   `POST /query`: To query relevant book content via vector search.
-   `POST /chat`: To interact with the RAG chatbot.

## Configuration

All sensitive configurations (API keys, database URLs) are loaded from `.env` files and managed via `src/config.py`. Refer to `.env.example` for required variables.

## Testing

Unit tests are located in `backend/tests/unit/` and integration tests in `backend/tests/integration/`. Run tests using `pytest`.

## Contributing

This backend is developed as part of the "Physical AI & Humanoid Robotics — Unified Book + RAG Chatbot" project. All changes must adhere to the project's constitution and maintain the additive and isolated nature of this backend service.
