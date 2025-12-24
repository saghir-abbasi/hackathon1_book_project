import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from src.main import app # Assuming app is imported from main for testing

# Fixture to override the AgentService for testing
@pytest.fixture
def mock_agent_service():
    with patch('app.agent.router.agent_service', new_callable=AsyncMock) as mock_service:
        # Mock the stream_chat_completions to yield predefined chunks
        async def mock_stream_response(*args, **kwargs):
            yield "Hello"
            yield " from "
            yield "test"
            yield " agent."
        
        mock_service.process_agent_stream.return_value = mock_stream_response()
        
        # Mock for the metadata endpoint
        mock_service.get_agent_metadata.return_value = {
            "chapters": [{"id": "test-chap-1", "title": "Test Chapter 1"}],
            "sections": [],
            "bookMetadata": {"title": "Test Book"}
        }
        
        yield mock_service

@pytest.mark.asyncio
async def test_stream_agent_query(mock_agent_service):
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "userQuery": "What is ROS 2?",
            "chapterId": "module-1-ros2-basics",
            "sessionId": "test-session-123",
            "userId": "test-user-456"
        }
        
        response = await client.post("/api/agent/query", json=payload)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream"
        
        full_response_content = ""
        # The StreamingResponse sends chunks as "data: {json}\n\n"
        async for chunk in response.aiter_bytes():
            decoded_chunk = chunk.decode('utf-8')
            full_response_content += decoded_chunk

        assert 'data: {"token": "Hello"}\n\n' in full_response_content
        assert 'data: {"token": " from "}\n\n' in full_response_content
        assert 'data: {"token": "test"}\n\n' in full_response_content
        assert 'data: {"token": " agent."}\n\n' in full_response_content
        assert 'data: {"event": "end", "token": ""}\n\n' in full_response_content
        
        mock_agent_service.process_agent_stream.assert_called_once_with(
            user_query="What is ROS 2?",
            chapter_id="module-1-ros2-basics",
            session_id="test-session-123",
            user_id="test-user-456",
            selected_text=None,
            last_model_messages=None
        )

@pytest.mark.asyncio
async def test_stream_agent_query_with_selected_text(mock_agent_service):
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "userQuery": "Explain this.",
            "chapterId": "module-1-ros2-basics",
            "sessionId": "test-session-123",
            "userId": "test-user-456",
            "selectedText": "ROS 2 is designed for distributed systems."
        }
        
        response = await client.post("/api/agent/query", json=payload)
        assert response.status_code == 200
        
        mock_agent_service.process_agent_stream.assert_called_once_with(
            user_query="Explain this.",
            chapter_id="module-1-ros2-basics",
            session_id="test-session-123",
            user_id="test-user-456",
            selected_text="ROS 2 is designed for distributed systems.",
            last_model_messages=None
        )

@pytest.mark.asyncio
async def test_stream_agent_query_rate_limit(mock_agent_service):
    # This test will require mocking the security middleware more directly
    # For now, we'll just test that the endpoint can be hit
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "userQuery": "Test rate limit",
            "chapterId": "module-1",
            "sessionId": "test-rl-session",
            "userId": "test-rl-user"
        }
        
        response = await client.post("/api/agent/query", json=payload)
        assert response.status_code == 200 # Should pass without hitting rate limit on first try

@pytest.mark.asyncio
async def test_get_agent_metadata():
    # The /api/agent/metadata endpoint uses mock data directly in the router for now
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/agent/metadata") # It's a POST according to spec
        
        assert response.status_code == 200
        data = response.json()
        assert "chapters" in data
        assert "sections" in data
        assert "bookMetadata" in data
        assert len(data["chapters"]) > 0
        assert data["chapters"][0]["id"] == "test-chap-1"
        assert data["bookMetadata"]["title"] == "Test Book"
