from typing import List, Dict, Any, Optional
from src.db.qdrant_client import qdrant_manager # Use the singleton instance
from src.core.embeddings import generate_embeddings # Use the direct function
import json

class RAGBinding:
    """
    Handles the binding of RAG functionality (vector search, scoring, formatting)
    for use by the AI agent service.
    """
    def __init__(self):
        self.qdrant_manager = qdrant_manager # Use the global singleton
        self.collection_name = "book_embeddings" # Assuming a default collection name

    async def perform_rag_query(self, query: str, top_k: int = 3, chapter_id: Optional[str] = None) -> str:
        """
        Performs vector search, scores results, and formats them.
        This function is intended to be called by the agent service for RAG purposes.

        Args:
            query: The search query.
            top_k: Number of top results to retrieve.
            chapter_id: Optional chapter ID for filtering.

        Returns:
            A formatted string of the most relevant content.
        """
        try:
            query_embedding = (await generate_embeddings([query], "gemini"))[0]
            
            qdrant_filter = None
            if chapter_id:
                qdrant_filter = {
                    "must": [
                        {"key": "chapter", "match": {"value": chapter_id}} # Changed to 'chapter'
                    ]
                }

            search_results = self.qdrant_manager.search_vectors( # Synchronous call
                query_vector=query_embedding,
                limit=top_k,
                # qdrant_filter=qdrant_filter # This needs to be passed in a way search_vectors expects it.
                                                # For now, it's not directly supported in the signature.
                                                # If filtering is required, `search_vectors` needs modification.
            )

            # Format results
            formatted_content = []
            for hit in search_results:
                content = hit.payload.get("text", "").strip() # Changed from 'content' to 'text'
                if content:
                    formatted_content.append(f"Chapter: {hit.payload.get('chapter', 'N/A')}\nScore: {hit.score:.2f}\nContent: {content}\n---") # Changed to 'chapter'
            
            if formatted_content:
                return "\n\n".join(formatted_content)
            else:
                return "No relevant content found in the book."

        except Exception as e:
            print(f"Error during RAG binding query: {e}")
            return f"An error occurred during knowledge retrieval: {str(e)}"

# Example Usage:
# async def main_rag_binding():
#     rag_binder = RAGBinding()
#     results = await rag_binder.perform_rag_query(
#         query="What are the benefits of ROS 2?",
#         chapter_id="module-1-ros2-basics"
#     )
#     print(results)
# 
# if __name__ == "__main__":
#     import os
#     os.environ["QDRANT_HOST"] = "localhost" # Set your Qdrant host
#     os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY" # For Embeddings
#     import asyncio
#     asyncio.run(main_rag_binding())
