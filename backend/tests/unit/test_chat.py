from fastapi.testclient import TestClient
from src.main import app
from src.models.chat_models import ChatRequest, ChatMessage
from unittest.mock import patch, AsyncMock
import pytest
from fastapi import status
import uuid
import datetime

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_dependencies_for_chat():
    with patch('src.api.chat_router.retrieve_relevant_segments') as mock_retrieve_segments, \
         patch('src.api.chat_router.generate_rag_response') as mock_generate_rag_response:
        
        # Mock retrieve_relevant_segments
        mock_retrieve_segments.return_value = [
            {"text": "context 1", "metadata": {"chapter": "intro"}, "score": 0.95}
        ]

        # Mock generate_rag_response
        mock_generate_rag_response.return_value = "This is a mock assistant response."

        yield {
            "mock_retrieve_segments": mock_retrieve_segments,
            "mock_generate_rag_response": mock_generate_rag_response
        }

def test_chat_with_rag_chatbot_new_session(mock_dependencies_for_chat):
    """
    Test chat interaction for a new session.
    """
    user_message = "Hello, what is this book about?"
    request_data = ChatRequest(user_message=user_message)

    response = client.post("/chat", json=request_data.model_dump())

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "session_id" in response_data
    assert uuid.UUID(response_data["session_id"]) # Check if it's a valid UUID
    assert response_data["assistant_response"] == "This is a mock assistant response."
    assert "chat_message_id" in response_data
    assert uuid.UUID(response_data["chat_message_id"])
    assert response_data["context_used"] == ["context 1"]

    mock_dependencies_for_chat["mock_retrieve_segments"].assert_called_once_with(user_message)
    mock_dependencies_for_chat["mock_generate_rag_response"].assert_called_once_with(
        user_message, mock_dependencies_for_chat["mock_retrieve_segments"].return_value
    )

def test_chat_with_rag_chatbot_existing_session(mock_dependencies_for_chat):
    """
    Test chat interaction for an existing session with chat history.
    """
    existing_session_id = uuid.uuid4()
    user_message = "Tell me more."
    chat_history = [
        ChatMessage(sender="user", text="First message", timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()),
        ChatMessage(sender="bot", text="First reply", timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat())
    ]
    request_data = ChatRequest(
        session_id=existing_session_id,
        user_message=user_message,
        chat_history=chat_history
    )

    response = client.post("/chat", json=request_data.model_dump())

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert uuid.UUID(response_data["session_id"]) == existing_session_id
    assert response_data["assistant_response"] == "This is a mock assistant response."
    assert response_data["context_used"] == ["context 1"]

    mock_dependencies_for_chat["mock_retrieve_segments"].assert_called_once_with(user_message)
    mock_dependencies_for_chat["mock_generate_rag_response"].assert_called_once_with(
        user_message, mock_dependencies_for_chat["mock_retrieve_segments"].return_value
    )

def test_chat_with_rag_chatbot_retrieve_segments_error(mock_dependencies_for_chat):
    """
    Test chat interaction when retrieving segments fails.
    """
    mock_dependencies_for_chat["mock_retrieve_segments"].side_effect = Exception("Qdrant retrieve error")
    user_message = "Test error."
    request_data = ChatRequest(user_message=user_message)

    response = client.post("/chat", json=request_data.model_dump())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Qdrant retrieve error" in response.json()["detail"]

def test_chat_with_rag_chatbot_rag_response_error(mock_dependencies_for_chat):
    """
    Test chat interaction when RAG response generation fails.
    """
    mock_dependencies_for_chat["mock_generate_rag_response"].side_effect = ValueError("LLM generation failed")
    user_message = "Test error."
    request_data = ChatRequest(user_message=user_message)

    response = client.post("/chat", json=request_data.model_dump())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "LLM generation failed" in response.json()["detail"]

