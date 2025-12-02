from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.models.query_models import QueryRequest
from unittest.mock import patch, AsyncMock
import pytest
from qdrant_client.models import PointStruct, ScoredPoint
from fastapi import status

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_dependencies_for_query():
    with patch('backend.src.api.query_router.qdrant_manager') as mock_qdrant_manager, \
         patch('backend.src.api.query_router.generate_embeddings') as mock_generate_embeddings:
        
        # Mock QdrantManager.search_vectors
        mock_qdrant_manager.search_vectors.return_value = [
            ScoredPoint(
                id="1", 
                payload={"text": "relevant chunk 1", "chapter": "intro"},
                score=0.9
            ),
            ScoredPoint(
                id="2", 
                payload={"text": "relevant chunk 2", "chapter": "chapter1"},
                score=0.85
            )
        ]

        # Mock embedding generation for the query
        mock_generate_embeddings.return_value = [[0.5]*1536] # Dummy query embedding

        yield {
            "mock_qdrant_manager": mock_qdrant_manager,
            "mock_generate_embeddings": mock_generate_embeddings
        }

def test_query_book_content_success(mock_dependencies_for_query):
    """
    Test successful querying of book content.
    """
    request_data = QueryRequest(question="What is the main topic of the book?")
    response = client.post("/query", json=request_data.model_dump())

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data["results"]) == 2
    assert response_data["results"][0]["text"] == "relevant chunk 1"
    assert response_data["results"][0]["metadata"]["chapter"] == "intro"
    assert response_data["results"][0]["score"] == 0.9

    mock_dependencies_for_query["mock_generate_embeddings"].assert_called_once_with(
        [request_data.question], "openai" # Assuming default openai
    )
    mock_dependencies_for_query["mock_qdrant_manager"].search_vectors.assert_called_once()

def test_query_book_content_no_results(mock_dependencies_for_query):
    """
    Test querying with no relevant results found.
    """
    mock_dependencies_for_query["mock_qdrant_manager"].search_vectors.return_value = []
    request_data = QueryRequest(question="Non-existent topic")

    response = client.post("/query", json=request_data.model_dump())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "No relevant content found." in response.json()["detail"]

def test_query_book_content_embedding_error(mock_dependencies_for_query):
    """
    Test querying when embedding generation fails.
    """
    mock_dependencies_for_query["mock_generate_embeddings"].side_effect = ValueError("Embedding API error")
    request_data = QueryRequest(question="Error during embedding")

    response = client.post("/query", json=request_data.model_dump())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Embedding API error" in response.json()["detail"]

def test_query_book_content_qdrant_error(mock_dependencies_for_query):
    """
    Test querying when Qdrant search fails.
    """
    mock_dependencies_for_query["mock_qdrant_manager"].search_vectors.side_effect = Exception("Qdrant connection error")
    request_data = QueryRequest(question="Qdrant fails")

    response = client.post("/query", json=request_data.model_dump())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Qdrant connection error" in response.json()["detail"]
