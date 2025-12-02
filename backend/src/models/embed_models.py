from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ContentChunk(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class EmbedRequest(BaseModel):
    content_chunks: List[ContentChunk]

class EmbedResponse(BaseModel):
    status: str
    embedded_count: int