from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="RAG Chatbot Backend API",
    description="API for managing book content embeddings, vector search, and chatbot interactions.",
    version="1.0.0",
)

# Configure CORS
# For local Docusaurus frontend, typically http://localhost:3000
# For GitHub Pages, you might need to specify your GitHub Pages domain
# Load CORS origins from environment variable, default to common development origin
# origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
# origins = [origin.strip() for origin in origins_str.split(",")]
# TODO: Integrate with config.py once implemented for more robust settings
origins = ["http://localhost:3000"] # Placeholder until config.py is ready


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Include routers here as they are developed
from .api import embed_router, query_router, chat_router
app.include_router(embed_router.router, prefix="/embed", tags=["Embeddings"])
app.include_router(query_router.router, prefix="/query", tags=["Query"])
app.include_router(chat_router.router, prefix="/chat", tags=["Chatbot"])
