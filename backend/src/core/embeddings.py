from typing import List, Dict, Any
import os
import google.generativeai as genai
# import anthropic # if using Claude
from ..config import settings
from tenacity import retry, wait_random_exponential, stop_after_attempt # For retry logic
import uuid # For generating UUIDs for Qdrant points

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Splits a given text into smaller, overlapping chunks.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The maximum size of each text chunk.
        chunk_overlap (int): The number of tokens to overlap between consecutive chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be a non-negative integer")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be less than chunk_size")

    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        if i + chunk_size >= len(words):
            break
        i += (chunk_size - chunk_overlap)
    return chunks

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def generate_gemini_embeddings(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a list of texts using the Gemini API."""
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = "models/text-embedding-004" # The recommended model for text embeddings

    result = await genai.embed_content_async(
        model=model,
        content=texts,
        task_type="retrieval_document"
    )
    return result['embedding']

async def generate_embeddings(texts: List[str], model_provider: str) -> List[List[float]]:
    """Generates embeddings for a list of texts using the specified model provider."""
    if model_provider.lower() == "gemini":
        return await generate_gemini_embeddings(texts)
    elif model_provider.lower() == "openai":
        raise NotImplementedError("OpenAI embeddings are no longer supported. Please use 'gemini'.")
    else:
        raise ValueError(f"Unsupported embedding model provider: {model_provider}")

def prepare_qdrant_points(chunks: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Prepares data into Qdrant PointStruct format."""
    from qdrant_client.models import PointStruct
    
    if not (len(chunks) == len(embeddings) == len(metadatas)):
        raise ValueError("Lengths of chunks, embeddings, and metadatas must match.")
    
    points = []
    for i, (chunk_text, embedding, metadata) in enumerate(zip(chunks, embeddings, metadatas)):
        # Ensure 'id' is part of metadata if available, or generate a UUID
        point_id = metadata.get("id", str(uuid.uuid4())) # Assuming metadata might contain an id
        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={"text": chunk_text, **metadata}
            )
        )
    return points
