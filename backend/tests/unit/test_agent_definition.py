import pytest
from unittest.mock import mock_open, patch
from app.agent.agent_definition import AssistantAgent

# Mock the file system for loading system prompt
@pytest.fixture
def mock_system_prompt_file():
    with patch("builtins.open", mock_open(read_data="Mock system prompt content.")) as mock_file:
        yield mock_file

def test_assistant_agent_initialization(mock_system_prompt_file):
    agent = AssistantAgent(
        name="TestAgent",
        description="A test agent",
        system_prompt_path="path/to/mock/primary.txt"
    )

    assert agent.name == "TestAgent"
    assert agent.description == "A test agent"
    assert agent.system_prompt == "Mock system prompt content."
    assert "temperature" in agent.model_config
    assert "max_tokens" in agent.model_config
    assert isinstance(agent.tools, list)
    assert len(agent.safety_constraints) > 0

def test_assistant_agent_default_system_prompt_on_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        agent = AssistantAgent(
            name="TestAgent",
            description="A test agent",
            system_prompt_path="non/existent/path.txt"
        )
        assert "helpful AI assistant" in agent.system_prompt

def test_register_tool():
    agent = AssistantAgent(
        name="TestAgent",
        description="A test agent",
        system_prompt_path="path/to/mock/primary.txt" # Path won't be opened in this test
    )
    mock_tool_spec = {"type": "function", "function": {"name": "test_tool"}}
    agent.register_tool(mock_tool_spec)
    assert len(agent.tools) == 1
    assert agent.tools[0] == mock_tool_spec

def test_get_agent_definition(mock_system_prompt_file):
    agent = AssistantAgent(
        name="TestAgent",
        description="A test agent",
        system_prompt_path="path/to/mock/primary.txt"
    )
    definition = agent.get_agent_definition()

    assert definition["name"] == "TestAgent"
    assert definition["description"] == "A test agent"
    assert definition["system_prompt"] == "Mock system prompt content."
    assert "model_config" in definition
    assert "tools" in definition
    assert "safety_constraints" in definition
