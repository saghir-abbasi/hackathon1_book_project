from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid

class ChatMessage(BaseModel):
    sender: str # "user" or "bot"
    text: str
    timestamp: str # ISO formatted string

class ChatRequest(BaseModel):
    session_id: Optional[uuid.UUID] = None
    user_message: str
    chat_history: Optional[List[ChatMessage]] = None
    selected_text: Optional[str] = None
    chapter_id: Optional[str] = None
    section_id: Optional[str] = None
    offsets: Optional[List[int]] = None

class ChatResponse(BaseModel):
    session_id: uuid.UUID
    assistant_response: str
    chat_message_id: uuid.UUID
    context_used: Optional[List[str]] = None