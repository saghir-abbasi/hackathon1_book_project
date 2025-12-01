# Research: Backend API Layer Technology Choices

**Date**: 2025-12-01
**Feature**: [Backend API Layer (FastAPI + Qdrant + Neon)](../spec.md)

## Decision: Python 3.9+ for Backend Development

-   **Rationale**: FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. Python is well-suited for AI/ML workloads, including embedding generation and RAG pipelines, due to its rich ecosystem of libraries. Version 3.9+ ensures access to recent language features and continued support.
-   **Alternatives Considered**: Node.js with Express/Fastify (less mature ecosystem for advanced AI/ML tasks), Go with Gin/Echo (strong performance but steeper learning curve for quick API development with AI components).

## Decision: pytest for Backend Testing

-   **Rationale**: pytest is a mature, full-featured Python testing framework that is widely adopted, easy to learn, and highly extensible. It allows for writing concise and readable tests, which aligns with the project's quality standards.
-   **Alternatives Considered**: unittest (Python's built-in module, but pytest offers more features and a simpler syntax).

## Decision: OpenAI/Claude Code Embeddings for RAG Pipeline

-   **Rationale**: These are leading models for generating high-quality text embeddings, crucial for effective vector search and context retrieval in the RAG pipeline. The specific choice between OpenAI and Claude can be parameterized via environment variables for flexibility.
-   **Alternatives Considered**: Open-source models (e.g., Sentence Transformers, Hugging Face models) – while viable, proprietary models often offer superior performance and ease of use for general-purpose text embeddings.

## Decision: Psycopg2-binary / SQLAlchemy for PostgreSQL Interaction

-   **Rationale**: Psycopg2-binary is the most popular PostgreSQL adapter for Python, providing robust and performant connectivity. SQLAlchemy is a powerful and flexible SQL toolkit and Object Relational Mapper (ORM) that simplifies database interactions, provides schema migration capabilities, and reduces boilerplate code for managing user sessions and chat history.
-   **Alternatives Considered**: raw `psycopg2` (requires compilation), other ORMs (e.g., PonyORM, PeeWee - less widely adopted or feature-rich than SQLAlchemy).
