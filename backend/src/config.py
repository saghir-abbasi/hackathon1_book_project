import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Base configuration
    PROJECT_NAME: str = "RAG Chatbot Backend API"
    PROJECT_VERSION: str = "1.0.0"

    # CORS origins
    CORS_ORIGINS: List[str] = ["http://localhost:3000"] # Default for local Docusaurus
    
    # Qdrant configuration
    QDRANT_HOST: str
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "book_embeddings"

    # Neon PostgreSQL configuration
    DATABASE_URL: str

    # Embedding Model Configuration
    EMBEDDING_MODEL_PROVIDER: str = "openai" # "openai" or "claude"
    OPENAI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore" # Ignore extra fields not defined in the model
    )

settings = Settings()
