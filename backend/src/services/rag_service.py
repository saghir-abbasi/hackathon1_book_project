from typing import List, Dict, Any, Optional
import openai
# import anthropic
from ..core.embeddings import generate_embeddings
from ..db.qdrant_client import qdrant_manager
from ..config import settings
from qdrant_client.models import PointStruct, FieldCondition, Filter, MatchValue
from tenacity import retry, wait_random_exponential, stop_after_attempt


def _is_placeholder_value(value: Optional[str]) -> bool:
    """Check if a value is a placeholder that should be ignored."""
    if not value:
        return True
    placeholder_indicators = ['placeholder', 'unknown', 'test', 'dummy']
    return any(indicator in value.lower() for indicator in placeholder_indicators)


async def retrieve_relevant_segments(
    query_text: str,
    limit: int = 5,
    chapter_id: Optional[str] = None,
    section_id: Optional[str] = None,
    selected_text: Optional[str] = None # Added selected_text
) -> List[Dict[str, Any]]:
    """
    Retrieves relevant book segments from Qdrant based on a query text and optional filters.
    If selected_text is provided, it's incorporated into the query for higher relevance.
    """
    # Incorporate selected_text into the query for embedding
    effective_query_text = query_text
    if selected_text:
        effective_query_text = f"{selected_text}. {query_text}"

    # Generate embedding for the effective query
    query_embedding = (await generate_embeddings([effective_query_text], settings.EMBEDDING_MODEL_PROVIDER))[0]

    # Build filter only for non-placeholder values
    _filter = None
    conditions = []
    if chapter_id and not _is_placeholder_value(chapter_id):
        conditions.append(FieldCondition(key="chapter_id", match=MatchValue(value=chapter_id)))
    if section_id and not _is_placeholder_value(section_id):
        conditions.append(FieldCondition(key="section_id", match=MatchValue(value=section_id)))

    if conditions:
        _filter = Filter(must=conditions)

    # Search in Qdrant
    search_results = qdrant_manager.search_vectors(
        query_vector=query_embedding,
        limit=limit,
        query_filter=_filter # Apply filter here (None if no valid filters)
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


async def generate_rag_response(
    query_text: str, 
    context_segments: List[Dict[str, Any]], 
    selected_text: Optional[str] = None
) -> str:
    """
    Assembles context and generates an assistant response using an LLM.
    Incorporates selected_text with higher priority if available.
    """
    context = "\n\n".join([seg["text"] for seg in context_segments])
    
    system_prompt = "You are a helpful assistant that answers questions based on the provided book content context."
    
    if selected_text:
        system_prompt += f" If the user has provided specific 'selected_text', answer using ONLY this text: '{selected_text}' unless the user explicitly requests additional context. If the answer is not in the selected text, say 'I cannot answer this question based on the selected text.' Otherwise, use the broader context."
    else:
        system_prompt += " If the answer is not in the context, say 'I cannot answer this question based on the provided context.'"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query_text}"}
    ]

    if settings.EMBEDDING_MODEL_PROVIDER.lower() == "openai": # Assuming we use the same provider for chat completions
        return await generate_openai_chat_completion(messages)
    # elif settings.EMBEDDING_MODEL_PROVIDER.lower() == "claude":
    #     # Claude chat completion logic here
    #     pass
    else:
        # Fallback for unsupported LLM provider, including selected_text in response if available
        response_content = f"Based on the context:\n{context}\n\n"
        if selected_text:
            response_content += f"Selected Text: '{selected_text}'\n\n"
        response_content += f"Your question was: '{query_text}'. (This is a dummy RAG response due to unsupported LLM provider)"
        return response_content
