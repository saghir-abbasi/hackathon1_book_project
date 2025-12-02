from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.models.embed_models import EmbedRequest, ContentChunk
from unittest.mock import patch, AsyncMock
import pytest


client = TestClient(app)

# Mock QdrantManager and embedding generation
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('backend.src.api.embed_router.qdrant_manager') as mock_qdrant_manager, \
         patch('backend.src.api.embed_router.generate_embeddings') as mock_generate_embeddings, \
         patch('backend.src.api.embed_router.prepare_qdrant_points') as mock_prepare_qdrant_points:
        
        # Mock QdrantManager
        mock_qdrant_manager.create_collection_if_not_exists = AsyncMock()
        mock_qdrant_manager.upsert_vectors = AsyncMock(return_value=AsyncMock(status="completed"))
        mock_qdrant_manager.search_vectors = AsyncMock(return_value=[]) # Will be mocked more specifically for query tests

        # Mock embedding generation
        mock_generate_embeddings.return_value = [[0.1]*1536, [0.2]*1536] # Dummy embeddings

        # Mock prepare_qdrant_points
        mock_prepare_qdrant_points.return_value = [
            {"id": "1", "vector": [0.1]*1536, "payload": {"text": "chunk1"}},
            {"id": "2", "vector": [0.2]*1536, "payload": {"text": "chunk2"}}
        ]
        yield

def test_embed_book_content_success():
    """
    Test successful embedding of book content.
    """
    content_chunks = [
        {"text": "This is a test chunk one.", "metadata": {"chapter": "intro"}},
        {"text": "This is a test chunk two.", "metadata": {"chapter": "intro"}}
    ]
    request_data = EmbedRequest(content_chunks=content_chunks)

    response = client.post("/embed", json=request_data.model_dump())

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"
    assert response.json()["embedded_count"] == len(content_chunks)

    # Verify mocks were called
    app.dependency_overrides[qdrant_manager].create_collection_if_not_exists.assert_called_once()
    app.dependency_overrides[generate_embeddings].assert_called_once_with(
        ["This is a test chunk one.", "This is a test chunk two."], "openai" # Assuming default openai
    )
    app.dependency_overrides[prepare_qdrant_points].assert_called_once()
    app.dependency_overrides[qdrant_manager].upsert_vectors.assert_called_once()

def test_embed_book_content_empty_input():
    """
    Test embedding with empty content chunks.
    """
    request_data = EmbedRequest(content_chunks=[])
    response = client.post("/embed", json=request_data.model_dump())

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"
    assert response.json()["embedded_count"] == 0

def test_embed_book_content_qdrant_failure(mock_dependencies):
    """
    Test embedding when Qdrant upsert fails.
    """
    mock_dependencies.qdrant_manager.upsert_vectors.return_value = AsyncMock(status="failed", error="some error")
    content_chunks = [
        {"text": "This is a test chunk one.", "metadata": {"chapter": "intro"}}
    ]
    request_data = EmbedRequest(content_chunks=content_chunks)

    response = client.post("/embed", json=request_data.model_dump())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Qdrant upsert failed" in response.json()["detail"]

def test_embed_book_content_embedding_generation_error(mock_dependencies):
    """
    Test embedding when embedding generation raises an error.
    """
    mock_dependencies.generate_embeddings.side_effect = ValueError("Embedding API error")
    content_chunks = [
        {"text": "This is a test chunk one.", "metadata": {"chapter": "intro"}}
    ]
    request_data = EmbedRequest(content_chunks=content_chunks)

    response = client.post("/embed", json=request_data.model_dump())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Embedding API error" in response.json()["detail"]
