import os

from app.agent.router import router as agent_router
from app.agent.security import AgentSecurityMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI(
    title="RAG Chatbot Backend API",
    description="API for managing book content embeddings, vector search, and chatbot interactions.",
    version="1.0.0",
)

# Configure CORS using settings from config.py with environment variable override
origins = settings.cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Agent Security Middleware
app.add_middleware(AgentSecurityMiddleware)


@app.on_event("startup")
async def startup_event():
    # Placeholder for database connection, Qdrant client initialization etc.
    print("Application startup complete.")


@app.on_event("shutdown")
async def shutdown_event():
    # Placeholder for database connection close, Qdrant client close etc.
    print("Application shutdown complete.")


# Root endpoint
@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend API is running!"}


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Favicon endpoint to prevent 404 errors
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)  # No content


# Additional favicon endpoint for PNG format to prevent 404 errors
@app.get("/favicon.png", include_in_schema=False)
async def favicon_png():
    from fastapi.responses import Response
    return Response(status_code=204)  # No content


# Include routers here as they are developed
from .api import chat_router, embed_router, query_router

app.include_router(embed_router.router, prefix="/embed", tags=["Embeddings"])
app.include_router(query_router.router, prefix="/query", tags=["Query"])
app.include_router(chat_router.router, prefix="/chat", tags=["Chatbot"])
app.include_router(agent_router, prefix="/api", tags=["Agent"])
