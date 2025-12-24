from app.agent.tools.rag_tool import RAGTool
from app.agent.tools.selected_text_tool import SelectedTextTool
from app.agent.tools.chapter_metadata_tool import ChapterMetadataTool
from app.agent.tools.safe_execution_tool import SafeExecutionTool # Now implemented

class ToolBindings:
    def __init__(self, assistant_agent: AssistantAgent):
        self.assistant_agent = assistant_agent
        self._initialize_tools()
        self._register_tools()

    def _initialize_tools(self):
        """Initializes all available tools."""
        self.rag_tool_instance = RAGTool()
        self.selected_text_tool_instance = SelectedTextTool()
        self.chapter_metadata_tool_instance = ChapterMetadataTool()
        self.safe_execution_tool_instance = SafeExecutionTool() # Initialize when implemented

    def _register_tools(self):
        """Registers tool specifications with the assistant agent."""
        self.assistant_agent.register_tool(self.rag_tool_instance.get_tool_spec())
        self.assistant_agent.register_tool(self.selected_text_tool_instance.get_tool_spec())
        self.assistant_agent.register_tool(self.chapter_metadata_tool_instance.get_tool_spec())
        self.assistant_agent.register_tool(self.safe_execution_tool_instance.get_tool_spec()) # Register when implemented

    def get_callable_tools(self):
        """
        Returns a dictionary of tool names mapped to their callable methods.
        This is used by the agent service to execute the tools.
        """
        return {
            "retrieve_book_content": self.rag_tool_instance.retrieve_book_content,
            "process_selected_text": self.selected_text_tool_instance.process_selected_text,
            "get_chapter_metadata": self.chapter_metadata_tool_instance.get_chapter_metadata,
            "safe_execute_code_snippet": self.safe_execution_tool_instance.safe_execute_code_snippet # Add when implemented
        }

# Example Usage:
# if __name__ == "__main__":
#     from app.agent.agent_definition import AssistantAgent
#     system_prompt_file = "backend/app/agent/system_prompts/primary.txt"
#     assistant_agent_instance = AssistantAgent(
#         name="RoboticsBookAssistant",
#         description="An AI assistant specializing in the 'Physical AI & Humanoid Robotics' book.",
#         system_prompt_path=system_prompt_file
#     )
#     tool_bindings = ToolBindings(assistant_agent_instance)
#
#     # Now the assistant_agent_instance has its tools registered
#     print("Registered Tools:", assistant_agent_instance.tools)
#     callable_tools = tool_bindings.get_callable_tools()
#     print("Callable Tool Names:", callable_tools.keys())
