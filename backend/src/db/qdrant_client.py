from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, ScoredPoint, PayloadSchemaType
from ..config import settings

class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_HOST,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=False # gRPC may have issues with certain cloud providers/proxies, falling back to HTTP/S
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def create_collection_if_not_exists(self, vector_size: int = 768): # Gemini's text-embedding-004 size
        collections_response = self.client.get_collections()
        existing_collections = [c.name for c in collections_response.collections]

        if self.collection_name not in existing_collections:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' created.")
            # Create payload indexes for filtering
            self.create_payload_indexes()
        else:
            print(f"Collection '{self.collection_name}' already exists.")

    def create_payload_indexes(self):
        """Create payload indexes for filtering on chapter_id and section_id."""
        try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter_id",
                field_schema=PayloadSchemaType.KEYWORD
            )
            print("Created payload index for 'chapter_id'")
        except Exception as e:
            print(f"Index for 'chapter_id' may already exist: {e}")

        try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="section_id",
                field_schema=PayloadSchemaType.KEYWORD
            )
            print("Created payload index for 'section_id'")
        except Exception as e:
            print(f"Index for 'section_id' may already exist: {e}")
            
    def upsert_vectors(self, points):
        # points expected to be in Qdrant's PointStruct format
        # e.g., points=[PointStruct(id=..., vector=..., payload={...})]
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )
        return operation_info
    
    def search_vectors(self, query_vector: list[float], limit: int = 5, score_threshold: float = 0.5, query_filter=None):
        """
        Search for similar vectors in the collection.

        Args:
            query_vector: The embedding vector to search for.
            limit: Maximum number of results to return.
            score_threshold: Minimum similarity score threshold.
            query_filter: Optional Qdrant Filter object for filtering results.

        Returns:
            List of search results with scores and payloads.
        """
        # Use query_points for qdrant-client >= 1.7.0
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter,
            with_payload=True
        )
        return search_result.points

qdrant_manager = QdrantManager()