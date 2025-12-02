from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from ..models.embed_models import EmbedRequest, EmbedResponse, ContentChunk
from ..core.embeddings import chunk_text, generate_embeddings, prepare_qdrant_points
from ..db.qdrant_client import qdrant_manager
from ..config import settings
import asyncio

router = APIRouter()

@router.post("/embed", response_model=EmbedResponse, status_code=status.HTTP_200_OK)
async def embed_book_content(request: EmbedRequest):
    """
    Accepts book content chunks, generates embeddings, and stores them in Qdrant.
    """
    total_embedded_count = 0
    try:
        # Ensure Qdrant collection exists
        qdrant_manager.create_collection_if_not_exists()

        texts_to_embed = [chunk.text for chunk in request.content_chunks]
        metadatas = [chunk.metadata if chunk.metadata else {} for chunk in request.content_chunks]
        
        # Generate embeddings
        embeddings = await generate_embeddings(texts_to_embed, settings.EMBEDDING_MODEL_PROVIDER)
        
        # Prepare points for Qdrant upsert
        qdrant_points = prepare_qdrant_points(texts_to_embed, embeddings, metadatas)
        
        # Upsert into Qdrant
        if qdrant_points:
            operation_info = qdrant_manager.upsert_vectors(qdrant_points)
            if operation_info.status == qdrant_client.models.UpdateStatus.COMPLETED:
                total_embedded_count = len(qdrant_points)
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Qdrant upsert failed: {operation_info.error}"
                )

        return EmbedResponse(status="success", embedded_count=total_embedded_count)

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
