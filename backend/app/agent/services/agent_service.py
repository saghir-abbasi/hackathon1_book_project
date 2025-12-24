import asyncio
import json
import logging
from typing import Any, AsyncGenerator, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from app.agent.agent_definition import AssistantAgent
from app.agent.runtime.metadata import Metadata

# Import RAG service for book content retrieval
from src.services.rag_service import retrieve_relevant_segments


class AgentService:
    def __init__(
        self, agent_definition_path: str = "backend/app/agent/agent_definition.py"
    ):
        from app.agent.runtime.gemini_client import GeminiClient
        from src.config import settings

        system_prompt_file = "backend/app/agent/system_prompts/primary.txt"
        self.assistant_agent = AssistantAgent(
            name="RoboticsBookAssistant",
            description="An AI assistant specializing in the 'Physical AI & Humanoid Robotics' book.",
            system_prompt_path=system_prompt_file,
        )

        model_config = self.assistant_agent.model_config
        self.gemini_client = GeminiClient(
            model_name=model_config.get("model_name", "gemini-2.5-flash"),
            api_key=settings.GEMINI_API_KEY,
        )

    async def _retrieve_rag_context(
        self,
        user_query: str,
        chapter_id: Optional[str] = None,
        selected_text: Optional[str] = None,
        limit: int = 5,
    ) -> str:
        """
        Retrieves relevant book content from the RAG system.

        Args:
            user_query: The user's question.
            chapter_id: Optional chapter ID to filter results.
            selected_text: Optional user-selected text for context.
            limit: Maximum number of segments to retrieve.

        Returns:
            Formatted context string from retrieved book segments.
        """
        try:
            # Use the rag_service to retrieve relevant segments
            segments = await retrieve_relevant_segments(
                query_text=user_query,
                limit=limit,
                chapter_id=chapter_id if chapter_id and chapter_id != "unknown" else None,
                selected_text=selected_text,
            )

            if not segments:
                logger.info("No relevant segments found in RAG retrieval.")
                return ""

            # Format segments into a context string
            context_parts = []
            for i, seg in enumerate(segments, 1):
                metadata = seg.get("metadata", {})
                chapter = metadata.get("chapter", metadata.get("chapter_id", "Unknown"))
                score = seg.get("score", 0)
                text = seg.get("text", "")

                context_parts.append(
                    f"[Source {i} - Chapter: {chapter}, Relevance: {score:.2f}]\n{text}"
                )

            context = "\n\n---\n\n".join(context_parts)
            logger.info(f"Retrieved {len(segments)} segments from RAG.")
            return context

        except Exception as e:
            logger.warning(f"RAG retrieval failed: {e}. Proceeding without book context.")
            return ""

    def _build_rag_prompt(
        self,
        user_query: str,
        rag_context: str,
        selected_text: Optional[str] = None,
    ) -> str:
        """
        Builds the prompt with RAG context for the LLM.

        Args:
            user_query: The user's question.
            rag_context: Retrieved context from the book.
            selected_text: Optional user-selected text.

        Returns:
            Formatted prompt string.
        """
        prompt_parts = []

        # Add system instructions
        prompt_parts.append(self.assistant_agent.system_prompt)
        prompt_parts.append("\n\n--- BOOK KNOWLEDGE BASE ---\n")

        # Add RAG context if available
        if rag_context:
            prompt_parts.append(
                "The following are relevant excerpts from the 'Physical AI & Humanoid Robotics' book. "
                "Use this information to answer the user's question accurately:\n\n"
            )
            prompt_parts.append(rag_context)
        else:
            prompt_parts.append(
                "No specific book content was found for this query. "
                "Please indicate if you cannot answer based on book content alone."
            )

        prompt_parts.append("\n\n--- USER QUERY ---\n")

        # Add selected text context if provided
        if selected_text:
            prompt_parts.append(
                f"The user has highlighted the following text and wants to ask about it:\n"
                f'"{selected_text}"\n\n'
            )

        prompt_parts.append(f"Question: {user_query}")

        prompt_parts.append(
            "\n\n--- INSTRUCTIONS ---\n"
            "1. Answer based ONLY on the book content provided above.\n"
            "2. If the answer is not in the provided context, say so clearly.\n"
            "3. Cite which source(s) you used when possible.\n"
            "4. Keep responses focused and relevant to robotics/AI topics."
        )

        return "".join(prompt_parts)

    async def process_agent_stream(
        self,
        user_query: str,
        chapter_id: str,
        session_id: str,
        user_id: str,
        selected_text: Optional[str] = None,
        last_model_messages: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Processes a user query using RAG retrieval and streams responses from Gemini.

        This method:
        1. Retrieves relevant book content from Qdrant via RAG
        2. Builds a context-aware prompt
        3. Streams the response from Gemini
        """
        logger.info(
            f"Processing query for session_id: {session_id}, chapter_id: {chapter_id}"
        )

        # Step 1: Retrieve relevant book content from RAG
        rag_context = await self._retrieve_rag_context(
            user_query=user_query,
            chapter_id=chapter_id,
            selected_text=selected_text,
            limit=5,
        )

        # Step 2: Build the RAG-enhanced prompt
        rag_prompt = self._build_rag_prompt(
            user_query=user_query,
            rag_context=rag_context,
            selected_text=selected_text,
        )

        # Step 3: Prepare conversation messages
        current_messages = []
        if last_model_messages:
            current_messages.extend(last_model_messages)

        current_messages.append({"role": "user", "content": rag_prompt})

        try:
            # Step 4: Stream completions from the Gemini client
            async for chunk in self.gemini_client.stream_chat_completions(
                messages=current_messages
            ):
                yield chunk

        except Exception as e:
            logger.error(f"Error streaming from Gemini: {e}", exc_info=True)
            raise e


# Example Usage:
# async def main_process_stream():
#     agent_service = AgentService()
#     async for token in agent_service.process_agent_stream(
#         user_query="What are the main components of ROS 2?",
#         chapter_id="module-1-ros2-basics",
#         session_id="test-session-123",
#         user_id="test-user-456"
#     ):
#         print(token, end="")
#
# if __name__ == "__main__":
#     import os
#     os.environ["OPENAI_API_KEY"] = "sk-..." # Set your API key for testing
#     asyncio.run(main_process_stream())
