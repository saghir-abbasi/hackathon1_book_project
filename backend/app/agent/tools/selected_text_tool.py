from typing import Dict, Any, Optional
import json

class SelectedTextTool:
    """
    Tool for processing and returning selected text from the frontend.
    This tool primarily validates and formats the selected text for the agent's use.
    """
    def get_tool_spec(self) -> Dict[str, Any]:
        """
        Returns the tool specification in OpenAI function-calling compatible format.
        """
        return {
            "type": "function",
            "function": {
                "name": "process_selected_text",
                "description": "Processes and validates text selected by the user in the frontend. Use this to incorporate specific user-highlighted content into your reasoning.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The exact text segment selected by the user."
                        },
                        "chapter_id": {
                            "type": "string",
                            "description": "The ID of the chapter from which the text was selected."
                        }
                    },
                    "required": ["text", "chapter_id"]
                }
            }
        }

    async def process_selected_text(self, text: str, chapter_id: str) -> str:
        """
        Validates the selected text and chapter ID. In a more complex scenario,
        this could involve further processing, summarization, or validation against
        the actual book content.

        Args:
            text: The text string selected by the user.
            chapter_id: The ID of the chapter where the text was selected.

        Returns:
            A JSON string indicating success and echoing the processed text,
            or an error message if validation fails.
        """
        if not text or not chapter_id:
            return json.dumps({"status": "error", "message": "Selected text or chapter ID cannot be empty."}))

        # Basic length validation (can be made more robust using security.py limits)
        if len(text) > 2000: # Example limit, should align with AGENT_SELECTED_TEXT_MAX_LENGTH
            return json.dumps({"status": "error", "message": "Selected text is too long."}))

        # In a real scenario, you might want to:
        # - Verify chapter_id against known chapters
        # - Perform OCR/NLP on text to ensure it's meaningful
        # - Store selected text for analytics or user history

        return json.dumps({
            "status": "success",
            "processed_text": text,
            "context_chapter_id": chapter_id,
            "message": "Selected text processed successfully."
        })

# Example Usage:
# async def main_selected_text_tool():
#     selected_tool = SelectedTextTool()
#     tool_spec = selected_tool.get_tool_spec()
#     print(json.dumps(tool_spec, indent=2))
#
#     result = await selected_tool.process_selected_text(
#         text="Robotics is an interdisciplinary field that integrates computer science and engineering.",
#         chapter_id="intro-to-robotics"
#     )
#     print("\nProcessed Selected Text:")
#     print(result)
#
#     error_result = await selected_tool.process_selected_text(text="", chapter_id="intro-to-robotics")
#     print("\nError Case:")
#     print(error_result)
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main_selected_text_tool())
