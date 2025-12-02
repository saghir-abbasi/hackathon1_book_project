from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any, Optional
from ..models.query_models import QueryRequest, QueryResponse, QueryResult
from ..core.embeddings import generate_embeddings
from ..db.qdrant_client import qdrant_manager
from ..config import settings
import asyncio

router = APIRouter()

@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_book_content(request: QueryRequest):
    """
    Accepts a user question, performs a vector search in Qdrant, and returns relevant text chunks.
    """
    try:
        # Generate embedding for the query question
        query_embedding = (await generate_embeddings([request.question], settings.EMBEDDING_MODEL_PROVIDER))[0]

        # Search in Qdrant
        search_results = qdrant_manager.search_vectors(
            query_vector=query_embedding,
            limit=request.limit,
            score_threshold=request.score_threshold
        )
        
        results = []
        for hit in search_results:
            results.append(QueryResult(
                text=hit.payload["text"],
                metadata={k: v for k, v in hit.payload.items() if k != "text"},
                score=hit.score
            ))

        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No relevant content found."
            )

        return QueryResponse(results=results)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
