import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.fixture
def mock_rag_segments():
    """Mock RAG segments returned by retrieve_relevant_segments."""
    return [
        {
            "text": "ROS 2 is the next generation Robot Operating System. It provides the tools, libraries, and conventions you need to develop robot applications.",
            "metadata": {"chapter": "ros2-basics", "section": "introduction"},
            "score": 0.92
        },
        {
            "text": "Nodes in ROS 2 are the fundamental units of computation. Each node performs a specific task.",
            "metadata": {"chapter": "ros2-basics", "section": "nodes"},
            "score": 0.88
        }
    ]


@pytest.fixture
def mock_gemini_response():
    """Mock streaming response from Gemini."""
    async def stream_response(*args, **kwargs):
        chunks = ["Based on", " the book content,", " ROS 2", " is a robotics framework."]
        for chunk in chunks:
            yield chunk
    return stream_response


@pytest.mark.asyncio
async def test_agent_service_retrieves_rag_context(mock_rag_segments, mock_gemini_response):
    """Test that AgentService retrieves RAG context before generating response."""
    with patch('app.agent.services.agent_service.retrieve_relevant_segments', new_callable=AsyncMock) as mock_retrieve, \
         patch('app.agent.runtime.gemini_client.GeminiClient') as MockGeminiClient, \
         patch('builtins.open', MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="System prompt")))))):

        # Setup mocks
        mock_retrieve.return_value = mock_rag_segments
        mock_gemini_instance = MockGeminiClient.return_value
        mock_gemini_instance.stream_chat_completions = mock_gemini_response

        from app.agent.services.agent_service import AgentService
        agent_service = AgentService()

        # Collect streamed response
        response_chunks = []
        async for chunk in agent_service.process_agent_stream(
            user_query="What is ROS 2?",
            chapter_id="module-1-ros2-basics",
            session_id="test-session",
            user_id="test-user"
        ):
            response_chunks.append(chunk)

        # Verify RAG retrieval was called
        mock_retrieve.assert_called_once()
        call_args = mock_retrieve.call_args
        assert call_args.kwargs['query_text'] == "What is ROS 2?"
        assert call_args.kwargs['chapter_id'] == "module-1-ros2-basics"

        # Verify response was generated
        assert len(response_chunks) > 0
        full_response = "".join(response_chunks)
        assert "ROS 2" in full_response


@pytest.mark.asyncio
async def test_agent_service_includes_selected_text_in_rag(mock_rag_segments, mock_gemini_response):
    """Test that selected_text is passed to RAG retrieval."""
    with patch('app.agent.services.agent_service.retrieve_relevant_segments', new_callable=AsyncMock) as mock_retrieve, \
         patch('app.agent.runtime.gemini_client.GeminiClient') as MockGeminiClient, \
         patch('builtins.open', MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="System prompt")))))):

        mock_retrieve.return_value = mock_rag_segments
        mock_gemini_instance = MockGeminiClient.return_value
        mock_gemini_instance.stream_chat_completions = mock_gemini_response

        from app.agent.services.agent_service import AgentService
        agent_service = AgentService()

        selected_text = "Nodes are fundamental computation units"

        async for _ in agent_service.process_agent_stream(
            user_query="Explain this",
            chapter_id="ros2-basics",
            session_id="test-session",
            user_id="test-user",
            selected_text=selected_text
        ):
            pass

        # Verify selected_text was passed to RAG
        call_args = mock_retrieve.call_args
        assert call_args.kwargs['selected_text'] == selected_text


@pytest.mark.asyncio
async def test_agent_service_handles_empty_rag_context(mock_gemini_response):
    """Test that AgentService handles gracefully when no RAG context is found."""
    with patch('app.agent.services.agent_service.retrieve_relevant_segments', new_callable=AsyncMock) as mock_retrieve, \
         patch('app.agent.runtime.gemini_client.GeminiClient') as MockGeminiClient, \
         patch('builtins.open', MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="System prompt")))))):

        # Return empty results
        mock_retrieve.return_value = []
        mock_gemini_instance = MockGeminiClient.return_value
        mock_gemini_instance.stream_chat_completions = mock_gemini_response

        from app.agent.services.agent_service import AgentService
        agent_service = AgentService()

        response_chunks = []
        async for chunk in agent_service.process_agent_stream(
            user_query="Random unrelated question",
            chapter_id="unknown",
            session_id="test-session",
            user_id="test-user"
        ):
            response_chunks.append(chunk)

        # Should still generate a response
        assert len(response_chunks) > 0


@pytest.mark.asyncio
async def test_agent_service_handles_rag_failure(mock_gemini_response):
    """Test that AgentService handles RAG retrieval failure gracefully."""
    with patch('app.agent.services.agent_service.retrieve_relevant_segments', new_callable=AsyncMock) as mock_retrieve, \
         patch('app.agent.runtime.gemini_client.GeminiClient') as MockGeminiClient, \
         patch('builtins.open', MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="System prompt")))))):

        # Simulate RAG failure
        mock_retrieve.side_effect = Exception("Qdrant connection failed")
        mock_gemini_instance = MockGeminiClient.return_value
        mock_gemini_instance.stream_chat_completions = mock_gemini_response

        from app.agent.services.agent_service import AgentService
        agent_service = AgentService()

        response_chunks = []
        async for chunk in agent_service.process_agent_stream(
            user_query="What is ROS 2?",
            chapter_id="ros2-basics",
            session_id="test-session",
            user_id="test-user"
        ):
            response_chunks.append(chunk)

        # Should still generate a response (graceful degradation)
        assert len(response_chunks) > 0


@pytest.mark.asyncio
async def test_build_rag_prompt_includes_context(mock_rag_segments):
    """Test that _build_rag_prompt properly includes RAG context."""
    with patch('builtins.open', MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="You are a helpful assistant.")))))), \
         patch('app.agent.runtime.gemini_client.GeminiClient'):

        from app.agent.services.agent_service import AgentService
        agent_service = AgentService()

        # Format context like _retrieve_rag_context does
        context_parts = []
        for i, seg in enumerate(mock_rag_segments, 1):
            chapter = seg["metadata"].get("chapter", "Unknown")
            score = seg.get("score", 0)
            text = seg.get("text", "")
            context_parts.append(f"[Source {i} - Chapter: {chapter}, Relevance: {score:.2f}]\n{text}")
        rag_context = "\n\n---\n\n".join(context_parts)

        prompt = agent_service._build_rag_prompt(
            user_query="What is ROS 2?",
            rag_context=rag_context,
            selected_text=None
        )

        # Verify prompt contains key elements
        assert "ROS 2" in prompt
        assert "BOOK KNOWLEDGE BASE" in prompt
        assert "ros2-basics" in prompt
        assert "Answer based ONLY on the book content" in prompt


@pytest.mark.asyncio
async def test_build_rag_prompt_with_selected_text():
    """Test that _build_rag_prompt includes selected text when provided."""
    with patch('builtins.open', MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=MagicMock(read=MagicMock(return_value="You are a helpful assistant.")))))), \
         patch('app.agent.runtime.gemini_client.GeminiClient'):

        from app.agent.services.agent_service import AgentService
        agent_service = AgentService()

        selected_text = "Nodes perform specific tasks"
        prompt = agent_service._build_rag_prompt(
            user_query="Explain this",
            rag_context="Some context about ROS 2",
            selected_text=selected_text
        )

        # Verify selected text is highlighted in prompt
        assert selected_text in prompt
        assert "highlighted the following text" in prompt
