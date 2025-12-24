from fastapi.testclient import TestClient
from src.main import app
from src.config import settings
from src.db.qdrant_client import QdrantManager
from src.db.database import create_db_and_tables, SessionLocal, engine, get_db
from src.db.base_class import Base # Import Base from its new location
from src.models.embed_models import EmbedRequest, ContentChunk
from src.models.query_models import QueryRequest
from src.models.chat_models import ChatRequest
from src.models.db_models import UserSession, ChatMessage # Import UserSession, ChatMessage
import pytest
import os
import time
import uuid # Add uuid import
from unittest.mock import patch, AsyncMock

client = TestClient(app)

# Fixture for Qdrant Manager (real client)
@pytest.fixture(scope="module")
def qdrant_test_manager():
    # Ensure test specific settings are used if necessary
    settings.QDRANT_HOST = os.getenv("TEST_QDRANT_HOST", "localhost")
    settings.QDRANT_API_KEY = os.getenv("TEST_QDRANT_API_KEY", None)
    settings.QDRANT_COLLECTION_NAME = "test_book_embeddings_" + str(uuid.uuid4()).replace("-", "")[:8]

    manager = QdrantManager()
    # Ensure collection is clean before tests
    try:
        manager.client.delete_collection(collection_name=manager.collection_name)
    except Exception:
        pass # Collection might not exist
    manager.create_collection_if_not_exists(vector_size=768) # Gemini's embedding size
    yield manager
    # Clean up collection after tests
    manager.client.delete_collection(collection_name=manager.collection_name)

# Fixture for Database Session (real DB connection)
@pytest.fixture(scope="module")
def db_test_session():
    # Ensure test specific settings are used
    settings.DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg2://user:password@localhost/testdb")
    
    # Create tables for tests
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after tests
        Base.metadata.drop_all(bind=engine)

# Fixture to mock embedding generation for faster tests
@pytest.fixture(autouse=True)
def mock_embedding_generation():
    with patch('src.core.embeddings.generate_gemini_embeddings') as mock_gemini_embeddings:
        mock_gemini_embeddings.return_value = [[0.1] * 768 for _ in range(2)] # Return dummy embeddings for 2 texts
        yield mock_gemini_embeddings

# --- Test Qdrant Connectivity and Embedding ---
def test_integration_qdrant_embed_and_query(qdrant_test_manager: QdrantManager, mock_embedding_generation):
    """
    Test embedding and querying in Qdrant.
    """
    # Use the actual QdrantManager instance
    app.dependency_overrides[QdrantManager] = lambda: qdrant_test_manager

    # Embed content
    content_chunks = [
        ContentChunk(text="The quick brown fox jumps over the lazy dog.", metadata={"source": "fable"}),
        ContentChunk(text="Artificial intelligence is transforming industries.", metadata={"source": "tech_blog"})
    ]
    embed_request = EmbedRequest(content_chunks=content_chunks)
    embed_response = client.post("/embed", json=embed_request.model_dump())

    assert embed_response.status_code == status.HTTP_200_OK
    assert embed_response.json()["embedded_count"] == 2
    
    # Query content
    query_request = QueryRequest(question="What is AI?", limit=1)
    query_response = client.post("/query", json=query_request.model_dump())

    assert query_response.status_code == status.HTTP_200_OK
    results = query_response.json()["results"]
    assert len(results) == 1
    assert "Artificial intelligence" in results[0]["text"]

    # Clean up override
    del app.dependency_overrides[QdrantManager]

# --- Test Neon DB Session Creation ---
def test_integration_neon_db_session_and_chat_history(db_test_session: Session):
    """
    Test creating a session and adding chat history.
    """
    # Override get_db to use our test session
    app.dependency_overrides[get_db] = lambda: db_test_session

    # Initial chat request (new session)
    chat_request = ChatRequest(user_message="Hi chatbot")
    chat_response = client.post("/chat", json=chat_request.model_dump())

    assert chat_response.status_code == status.HTTP_200_OK
    session_id = chat_response.json()["session_id"]
    assistant_response = chat_response.json()["assistant_response"]

    # Verify session in DB
    session_in_db = db_test_session.query(UserSession).filter(UserSession.session_id == uuid.UUID(session_id)).first()
    assert session_in_db is not None
    assert len(session_in_db.chat_messages) == 2 # User + Bot message

    # Verify messages in DB
    history_in_db = db_test_session.query(ChatMessage).filter(ChatMessage.session_id == uuid.UUID(session_id)).order_by(ChatMessage.timestamp).all()
    assert history_in_db[0].text == "Hi chatbot"
    assert history_in_db[1].text == assistant_response

    # Clean up override
    del app.dependency_overrides[get_db]

# --- Test End-to-End Chat (using mocks for external LLM/Embeddings but real Qdrant/DB) ---
def test_integration_chat_end_to_end_mocked_llm(qdrant_test_manager: QdrantManager, db_test_session: Session, mock_embedding_generation):
    """
    Test a full chat interaction with mocked LLM but real Qdrant/DB.
    """
    app.dependency_overrides[QdrantManager] = lambda: qdrant_test_manager
    app.dependency_overrides[get_db] = lambda: db_test_session
    
    # Mock RAG service components for chat endpoint specifically
    with patch('src.services.rag_service.generate_rag_response') as mock_generate_rag:
        mock_generate_rag.return_value = "Mocked LLM final answer."

        user_message = "Tell me about RAG."
        chat_request = ChatRequest(user_message=user_message)
        chat_response = client.post("/chat", json=chat_request.model_dump())

        assert chat_response.status_code == status.HTTP_200_OK
        response_data = chat_response.json()
        assert response_data["assistant_response"] == "Mocked LLM final answer."
        assert "context_used" in response_data and len(response_data["context_used"]) > 0
        
        # Verify call to generate_rag_response included context
        mock_generate_rag.assert_called_once()
        args, _ = mock_generate_rag.call_args
        assert args[0] == user_message
        assert len(args[1]) > 0 # Should have context segments

    del app.dependency_overrides[QdrantManager]
    del app.dependency_overrides[get_db]
