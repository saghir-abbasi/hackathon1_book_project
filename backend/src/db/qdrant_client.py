from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from ..config import settings

class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True # Recommended for better performance
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def create_collection_if_not_exists(self, vector_size: int = 1536): # OpenAI's default embedding size
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' created.")
        else:
            print(f"Collection '{self.collection_name}' already exists.")
            
    def upsert_vectors(self, points):
        # points expected to be in Qdrant's PointStruct format
        # e.g., points=[PointStruct(id=..., vector=..., payload={...})]
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )
        return operation_info
    
    def search_vectors(self, query_vector: list[float], limit: int = 5, score_threshold: float = 0.7):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        return search_result

qdrant_manager = QdrantManager()