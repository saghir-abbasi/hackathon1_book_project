from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    question: str
    limit: int = 5
    score_threshold: float = 0.7

class QueryResult(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None
    score: float

class QueryResponse(BaseModel):
    results: List[QueryResult]