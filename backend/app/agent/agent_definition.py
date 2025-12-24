from typing import Any, Dict, List, Optional


class AssistantAgent:
    def __init__(self, name: str, description: str, system_prompt_path: str):
        self.name = name
        self.description = description
        self.system_prompt = self._load_system_prompt(system_prompt_path)
        self.model_config = self._get_default_model_config()
        self.tools: List[Dict[str, Any]] = []  # To be populated by tool_bindings
        self.safety_constraints: List[str] = self._get_default_safety_constraints()

    def _load_system_prompt(self, path: str) -> str:
        # In a real scenario, this would load from a file or database
        # For now, we'll hardcode or load a placeholder
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return (
                "You are a helpful AI assistant. Your response about robotics and AI "
            )

    def _get_default_model_config(self) -> Dict[str, Any]:
        # Configuration for the Gemini model
        return {
            "model_name": "gemini-2.5-flash",  # Use a valid Gemini model
            "temperature": 0.8,
            "max_output_tokens": 1024,  # Renamed from max_tokens for clarity
            "top_p": 1,
            "stream": True,
            "retry_attempts": 3,
            "retry_delay_base": 1.0,  # seconds
        }

    def _get_default_safety_constraints(self) -> List[str]:
        return [
            "MUST NOT generate harmful content.",
            "MUST NOT provide medical, legal, or financial advice.",
            "MUST NOT execute arbitrary code.",
            # "MUST NOT respond to queries outside the domain of the book's content.",
        ]

    def register_tool(self, tool_spec: Dict[str, Any]):
        """Registers a tool specification with the agent."""
        self.tools.append(tool_spec)

    def get_agent_definition(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the agent's definition."""
        return {
            "name": self.name,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "model_config": self.model_config,
            "tools": self.tools,
            "safety_constraints": self.safety_constraints,
        }


# Example of how to instantiate the agent
# system_prompt_file = "backend/app/agent/system_prompts/primary.txt"
# assistant_agent = AssistantAgent(
#     name="RoboticsBookAssistant",
#     description="An AI assistant specializing in the 'Physical AI & Humanoid Robotics' book.",
#     system_prompt_path=system_prompt_file
# )
