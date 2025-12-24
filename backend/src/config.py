import json
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

    # CORS origins - load from environment variable or use defaults
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",           # Local Docusaurus development
        "http://localhost:3001",           # Alternative Docusaurus port
        "https://localhost:3000",          # HTTPS local development
        "https://localhost:3001",          # HTTPS alternative port
        "https://book-project-backend.vercel.app",  # Backend deployment (for testing)
        "https://your-username.github.io", # Replace with your actual GitHub Pages URL
        "https://*.vercel.app"             # For Vercel deployments
    ]

    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins from environment variable or use defaults."""
        cors_env = os.getenv("CORS_ORIGINS")
        if cors_env:
            # Handle both JSON array format and comma-separated string format
            cors_env = cors_env.strip()
            if cors_env.startswith('[') and cors_env.endswith(']'):
                # Try to parse as JSON array
                try:
                    return json.loads(cors_env)
                except json.JSONDecodeError:
                    # If JSON parsing fails, fall back to comma-separated parsing
                    pass
            # Parse as comma-separated values
            return [origin.strip() for origin in cors_env.split(",")]
        return self.CORS_ORIGINS
    
    # Qdrant configuration
    QDRANT_HOST: str
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "book_embeddings"

    # Neon PostgreSQL configuration
    DATABASE_URL: str

    # Embedding Model Configuration
    EMBEDDING_MODEL_PROVIDER: str = "gemini" # "gemini", "openai", or "claude"
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore" # Ignore extra fields not defined in the model
    )

settings = Settings()
