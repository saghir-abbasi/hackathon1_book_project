from typing import Dict, Any, List, Optional
import json

class ChapterMetadataTool:
    """
    Tool for retrieving metadata about book chapters.
    This tool simulates access to a database or API that holds chapter information.
    """
    def __init__(self):
        # Placeholder for a real chapter metadata store.
        # In a full implementation, this would connect to a DB or read from a structured file.
        self.chapter_db = self._load_mock_chapter_data()

    def _load_mock_chapter_data(self) -> Dict[str, Any]:
        """
        Loads mock chapter data for demonstration purposes.
        """
        return {
            "module-1-ros2-basics": {
                "title": "ROS 2 Basics",
                "module": "Robotic Nervous System",
                "description": "Introduction to Robot Operating System 2 concepts and architecture.",
                "tags": ["ROS2", "Robotics", "Middleware"],
                "word_count": 5000
            },
            "module-1-urdf-fundamentals": {
                "title": "URDF Fundamentals",
                "module": "Robotic Nervous System",
                "description": "Understanding Universal Robot Description Format for robot modeling.",
                "tags": ["URDF", "Robot Modeling", "Simulation"],
                "word_count": 3500
            },
            "module-2-gazebo-physics": {
                "title": "Gazebo Physics",
                "module": "Digital Twin",
                "description": "Deep dive into physics simulation within Gazebo for robotics.",
                "tags": ["Gazebo", "Simulation", "Physics"],
                "word_count": 6000
            },
            "module-3-isaac-sim-basics": {
                "title": "Isaac Sim Basics",
                "module": "AI Robot Brain",
                "description": "Getting started with NVIDIA Isaac Sim for robotics simulation and AI.",
                "tags": ["Isaac Sim", "NVIDIA", "Simulation", "AI"],
                "word_count": 7000
            }
        }

    def get_tool_spec(self) -> Dict[str, Any]:
        """
        Returns the tool specification in OpenAI function-calling compatible format.
        """
        return {
            "type": "function",
            "function": {
                "name": "get_chapter_metadata",
                "description": "Retrieves detailed metadata for a specific book chapter or lists all available chapters. Use this to find information about chapter titles, descriptions, and modules.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "chapter_id": {
                            "type": "string",
                            "nullable": True,
                            "description": "Optional: The ID of the specific chapter to retrieve metadata for. If not provided, returns a list of all available chapters."
                        }
                    }
                }
            }
        }

    async def get_chapter_metadata(self, chapter_id: Optional[str] = None) -> str:
        """
        Retrieves metadata for a given chapter_id or lists all available chapters.

        Args:
            chapter_id: The ID of the chapter to look up.

        Returns:
            A JSON string containing the chapter's metadata or a list of all chapters.
        """
        if chapter_id:
            metadata = self.chapter_db.get(chapter_id)
            if metadata:
                return json.dumps({"status": "success", "chapter_metadata": metadata}, indent=2)
            else:
                return json.dumps({"status": "error", "message": f"Chapter '{chapter_id}' not found."}, indent=2)
        else:
            # Return a summary of all chapters if no specific ID is requested
            chapter_list_summary = [
                {"id": chap_id, "title": data["title"], "module": data["module"]}
                for chap_id, data in self.chapter_db.items()
            ]
            return json.dumps({"status": "success", "all_chapters_summary": chapter_list_summary}, indent=2)

# Example Usage:
# async def main_chapter_metadata_tool():
#     chapter_tool = ChapterMetadataTool()
#     tool_spec = chapter_tool.get_tool_spec()
#     print(json.dumps(tool_spec, indent=2))
#
#     # Get metadata for a specific chapter
#     ros2_metadata = await chapter_tool.get_chapter_metadata(chapter_id="module-1-ros2-basics")
#     print("\nROS 2 Chapter Metadata:")
#     print(ros2_metadata)
#
#     # Get list of all chapters
#     all_chapters = await chapter_tool.get_chapter_metadata()
#     print("\nAll Chapters Summary:")
#     print(all_chapters)
#
#     # Test non-existent chapter
#     non_existent = await chapter_tool.get_chapter_metadata(chapter_id="non-existent-chapter")
#     print("\nNon-existent Chapter:")
#     print(non_existent)
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main_chapter_metadata_tool())
