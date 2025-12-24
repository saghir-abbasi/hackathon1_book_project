from typing import Dict, Any, Optional

class Metadata:
    """
    Helper class for preparing and validating metadata packets for agent requests.
    """
    @staticmethod
    def prepare_metadata(
        chapter_id: str,
        session_id: str,
        user_id: str,
        selected_text: Optional[str] = None,
        last_model_messages: Optional[list] = None,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Prepares a metadata packet for an agent request.

        Args:
            chapter_id: The ID of the current book chapter.
            session_id: The ID of the current chat session.
            user_id: The ID of the interacting user.
            selected_text: Optional text selected by the user in the frontend.
            last_model_messages: Optional list of previous messages for context.
            timestamp: Optional ISO formatted timestamp of the request.

        Returns:
            A dictionary containing the prepared metadata.
        """
        metadata_packet = {
            "chapter_id": chapter_id,
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": timestamp if timestamp else Metadata._generate_timestamp()
        }
        if selected_text:
            metadata_packet["selected_text"] = selected_text
        if last_model_messages:
            metadata_packet["last_model_messages"] = last_model_messages

        # Add any additional system-level metadata here
        metadata_packet["system_info"] = {
            "feature_version": "2.4",
            "agent_type": "openai-chatkit"
        }

        return metadata_packet

    @staticmethod
    def validate_metadata(metadata: Dict[str, Any]) -> bool:
        """
        Validates the structure and content of a metadata packet.
        This is a placeholder for more comprehensive validation logic.

        Args:
            metadata: The metadata packet to validate.

        Returns:
            True if the metadata is valid, False otherwise.
        """
        required_keys = ["chapter_id", "session_id", "user_id"]
        if not all(key in metadata for key in required_keys):
            return False
        
        # Add length checks, type checks, and other validations here
        if "selected_text" in metadata and not isinstance(metadata["selected_text"], str):
            return False
        
        return True

    @staticmethod
    def _generate_timestamp() -> str:
        """Generates an ISO formatted timestamp."""
        import datetime
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

# Example usage:
# metadata_packet = Metadata.prepare_metadata(
#     chapter_id="module-1-ros2-basics",
#     session_id="chat-abc-123",
#     user_id="user-xyz",
#     selected_text="ROS 2 is the Robot Operating System 2",
#     last_model_messages=[{"role": "user", "content": "What is ROS?"}]
# )
# print(metadata_packet)
# print(Metadata.validate_metadata(metadata_packet))
