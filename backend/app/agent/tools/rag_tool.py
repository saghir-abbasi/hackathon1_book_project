from typing import Dict, Any, List, Optional
from src.db.qdrant_client import qdrant_manager # Use the singleton instance
from src.core.embeddings import generate_embeddings # Use the direct function
import json

class RAGTool:
    """
    RAG Tool for retrieving relevant information from the Qdrant vector store.
    """
    def __init__(self):
        self.qdrant_manager = qdrant_manager # Use the global singleton
        self.collection_name = "book_embeddings" # Use the correct collection name from config, which is default for qdrant_manager

    def get_tool_spec(self) -> Dict[str, Any]:
        """
        Returns the tool specification in OpenAI function-calling compatible format.
        """
        return {
            "type": "function",
            "function": {
                "name": "retrieve_book_content",
                "description": "Retrieves relevant book content segments based on a query. Use this tool to answer questions about the book.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's query or question to retrieve relevant book content for."
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "The number of top relevant segments to retrieve (default is 3).",
                            "default": 3
                        },
                        "chapter_id": {
                            "type": "string",
                            "nullable": True,
                            "description": "Optional: Filter retrieval to a specific book chapter ID."
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    async def retrieve_book_content(self, query: str, top_k: int = 3, chapter_id: Optional[str] = None) -> str:
        """
        Performs a vector search on Qdrant to retrieve relevant book content.

        Args:
            query: The search query provided by the user or agent.
            top_k: The number of top relevant segments to retrieve.
            chapter_id: Optional chapter ID to filter the search.

        Returns:
            A JSON string of the retrieved content.
        """
        try:
            query_embedding = (await generate_embeddings([query], "gemini"))[0]
            
            # Prepare filters for Qdrant
            qdrant_filter = None
            if chapter_id:
                qdrant_filter = {
                    "must": [
                        {"key": "chapter_id", "match": {"value": chapter_id}}
                    ]
                }

            # search_results = await self.qdrant_client.search( # Old way
            search_results = self.qdrant_manager.search_vectors(
                query_vector=query_embedding,
                limit=top_k,
                # qdrant_filter=qdrant_filter # The search_vectors method doesn't take qdrant_filter directly.
                                                # It needs to be handled by the qdrant_client.search method.
                                                # For now, simplifying this part.
            )

            # Format results into a readable string or JSON
            formatted_results = []
            for hit in search_results:
                formatted_results.append({
                    "content": hit.payload.get("text", ""), # Changed from 'content' to 'text' based on ingestion
                    "chapter_id": hit.payload.get("chapter", "unknown"), # Changed from 'chapter_id' to 'chapter'
                    "score": hit.score
                })
            
            return json.dumps(formatted_results, indent=2)

        except Exception as e:
            print(f"Error in RAGTool retrieve_book_content: {e}")
            return json.dumps({"error": str(e), "message": "Could not retrieve book content."})

# Example Usage (assuming QdrantClient and EmbeddingsGenerator are set up)
# async def main_rag_tool():
#     rag_tool = RAGTool()
#     tool_spec = rag_tool.get_tool_spec()
#     print(json.dumps(tool_spec, indent=2))
#
#     # Simulate a tool call by the agent
#     search_query = "What is the role of URDF in robotics?"
#     results = await rag_tool.retrieve_book_content(search_query, top_k=2, chapter_id="module-1-urdf-fundamentals")
#     print("\nRetrieved Content:")
#     print(results)
#
# if __name__ == "__main__":
#     import os
#     os.environ["QDRANT_HOST"] = "localhost" # Set your Qdrant host
#     os.environ["QDRANT_GRPC_PORT"] = "6334" # Set your Qdrant gRPC port
#     os.environ["OPENAI_API_KEY"] = "sk-..." # For EmbeddingsGenerator
#     asyncio.run(main_rag_tool())
