from typing import List, Dict, Any
import openai
# import anthropic
from ..core.embeddings import generate_embeddings
from ..db.qdrant_client import qdrant_manager
from ..config import settings
from qdrant_client.models import PointStruct
from tenacity import retry, wait_random_exponential, stop_after_attempt


async def retrieve_relevant_segments(query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieves relevant book segments from Qdrant based on a query text.
    """
    # Generate embedding for the query
    query_embedding = (await generate_embeddings([query_text], settings.EMBEDDING_MODEL_PROVIDER))[0]

    # Search in Qdrant
    search_results = qdrant_manager.search_vectors(
        query_vector=query_embedding,
        limit=limit
    )

    # Extract relevant segments and their metadata
    relevant_segments = []
    for hit in search_results:
        relevant_segments.append({
            "text": hit.payload["text"],
            "metadata": {k: v for k, v in hit.payload.items() if k != "text"},
            "score": hit.score
        })
    
    return relevant_segments

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def generate_openai_chat_completion(
    messages: List[Dict[str, str]], 
    model: str = "gpt-3.5-turbo", 
    temperature: float = 0.7
) -> str:
    """Generates a chat completion using OpenAI API."""
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in environment variables.")
    
    openai.api_key = settings.OPENAI_API_KEY
    
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


async def generate_rag_response(query_text: str, context_segments: List[Dict[str, Any]]) -> str:
    """
    Assembles context and generates an assistant response using an LLM.
    """
    context = "\n\n".join([seg["text"] for seg in context_segments])
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided book content context. If the answer is not in the context, say 'I cannot answer this question based on the provided context.'"},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query_text}"}
    ]

    if settings.EMBEDDING_MODEL_PROVIDER.lower() == "openai": # Assuming we use the same provider for chat completions
        return await generate_openai_chat_completion(messages)
    # elif settings.EMBEDDING_MODEL_PROVIDER.lower() == "claude":
    #     # Claude chat completion logic here
    #     pass
    else:
        return f"Based on the context:\n{context}\n\nYour question was: '{query_text}'. (This is a dummy RAG response due to unsupported LLM provider)"
