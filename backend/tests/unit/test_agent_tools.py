import pytest
import json
from unittest.mock import AsyncMock, patch
from app.agent.tools.rag_tool import RAGTool
from app.agent.tools.selected_text_tool import SelectedTextTool
from app.agent.tools.chapter_metadata_tool import ChapterMetadataTool
from app.agent.tools.safe_execution_tool import SafeExecutionTool

# Mock external dependencies for RAGTool
@pytest.fixture
def mock_rag_dependencies():
    with patch('app.db.qdrant_client.QdrantClient') as MockQdrantClient, \
         patch('app.core.embeddings.EmbeddingsGenerator') as MockEmbeddingsGenerator:
        
        mock_qdrant_instance = MockQdrantClient.return_value
        mock_qdrant_instance.search = AsyncMock(return_value=[
            type('obj', (object,), {'payload': {'content': 'ROS 2 is a middleware for robotics.', 'chapter_id': 'ros2-basics'}, 'score': 0.9}),
            type('obj', (object,), {'payload': {'content': 'It provides services like messaging.', 'chapter_id': 'ros2-basics'}, 'score': 0.8})
        ])
        
        mock_embeddings_instance = MockEmbeddingsGenerator.return_value
        mock_embeddings_instance.generate_embedding = AsyncMock(return_value=[0.1]*768) # Updated embedding size
        
        yield mock_qdrant_instance, mock_embeddings_instance

@pytest.mark.asyncio
async def test_rag_tool_retrieve_book_content(mock_rag_dependencies):
    rag_tool = RAGTool()
    results_json = await rag_tool.retrieve_book_content("What is ROS 2?")
    results = json.loads(results_json)
    
    assert len(results) == 2
    assert "ROS 2 is a middleware for robotics." in results[0]["content"]
    assert results[0]["chapter_id"] == "ros2-basics"
    assert results[0]["score"] > 0
    
    rag_tool.qdrant_client.search.assert_called_once()
    rag_tool.embeddings_generator.generate_embedding.assert_called_once_with("What is ROS 2?")

@pytest.mark.asyncio
async def test_rag_tool_retrieve_book_content_with_chapter_id(mock_rag_dependencies):
    rag_tool = RAGTool()
    await rag_tool.retrieve_book_content("URDF basics", chapter_id="urdf-fundamentals")
    
    args, kwargs = rag_tool.qdrant_client.search.call_args
    assert kwargs['query_filter'] is not None
    assert kwargs['query_filter']['must'][0]['key'] == 'chapter_id'
    assert kwargs['query_filter']['must'][0]['match']['value'] == 'urdf-fundamentals'

def test_selected_text_tool_get_tool_spec():
    tool = SelectedTextTool()
    spec = tool.get_tool_spec()
    assert spec["type"] == "function"
    assert spec["function"]["name"] == "process_selected_text"
    assert "text" in spec["function"]["parameters"]["properties"]

@pytest.mark.asyncio
async def test_selected_text_tool_process_selected_text():
    tool = SelectedTextTool()
    result_json = await tool.process_selected_text("Some selected text", "chapter-1")
    result = json.loads(result_json)
    assert result["status"] == "success"
    assert result["processed_text"] == "Some selected text"

@pytest.mark.asyncio
async def test_selected_text_tool_process_selected_text_empty_input():
    tool = SelectedTextTool()
    result_json = await tool.process_selected_text("", "chapter-1")
    result = json.loads(result_json)
    assert result["status"] == "error"
    assert "cannot be empty" in result["message"]

def test_chapter_metadata_tool_get_tool_spec():
    tool = ChapterMetadataTool()
    spec = tool.get_tool_spec()
    assert spec["type"] == "function"
    assert spec["function"]["name"] == "get_chapter_metadata"
    assert "chapter_id" in spec["function"]["parameters"]["properties"]

@pytest.mark.asyncio
async def test_chapter_metadata_tool_get_chapter_metadata_specific():
    tool = ChapterMetadataTool()
    result_json = await tool.get_chapter_metadata("module-1-ros2-basics")
    result = json.loads(result_json)
    assert result["status"] == "success"
    assert result["chapter_metadata"]["title"] == "ROS 2 Basics"

@pytest.mark.asyncio
async def test_chapter_metadata_tool_get_chapter_metadata_all():
    tool = ChapterMetadataTool()
    result_json = await tool.get_chapter_metadata()
    result = json.loads(result_json)
    assert result["status"] == "success"
    assert len(result["all_chapters_summary"]) > 1

@pytest.mark.asyncio
async def test_chapter_metadata_tool_get_chapter_metadata_not_found():
    tool = ChapterMetadataTool()
    result_json = await tool.get_chapter_metadata("non-existent-chapter")
    result = json.loads(result_json)
    assert result["status"] == "error"
    assert "not found" in result["message"]

def test_safe_execution_tool_get_tool_spec():
    tool = SafeExecutionTool()
    spec = tool.get_tool_spec()
    assert spec["type"] == "function"
    assert spec["function"]["name"] == "safe_execute_code_snippet"
    assert "language" in spec["function"]["parameters"]["properties"]
    assert "code_snippet_id" in spec["function"]["parameters"]["properties"]

@pytest.mark.asyncio
async def test_safe_execution_tool_safe_execute_code_snippet_approved():
    tool = SafeExecutionTool()
    result_json = await tool.safe_execute_code_snippet("python", "ros2_node_creation_example")
    result = json.loads(result_json)
    assert result["status"] == "success"
    assert "Node 'my_robot_node' created successfully." in result["result"]

@pytest.mark.asyncio
async def test_safe_execution_tool_safe_execute_code_snippet_with_inputs():
    tool = SafeExecutionTool()
    result_json = await tool.safe_execute_code_snippet("python", "urdf_joint_calc", inputs={"angle": 90.0})
    result = json.loads(result_json)
    assert result["status"] == "success"
    assert "100.0" in result["result"] # 90 + 10

@pytest.mark.asyncio
async def test_safe_execution_tool_safe_execute_code_snippet_not_approved():
    tool = SafeExecutionTool()
    result_json = await tool.safe_execute_code_snippet("python", "malicious_code")
    result = json.loads(result_json)
    assert result["status"] == "error"
    assert "not pre-approved" in result["message"]

@pytest.mark.asyncio
async def test_safe_execution_tool_safe_execute_code_snippet_unsupported_language():
    tool = SafeExecutionTool()
    result_json = await tool.safe_execute_code_snippet("java", "ros2_node_creation_example")
    result = json.loads(result_json)
    assert result["status"] == "error"
    assert "not supported" in result["message"]
