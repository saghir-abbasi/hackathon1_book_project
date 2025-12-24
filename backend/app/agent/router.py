from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
import json

from app.agent.services.agent_service import AgentService
from app.agent.security import AgentSecurityMiddleware # To be applied at app level

router = APIRouter()
agent_service = AgentService() # Initialize your agent service

class AgentQueryRequest(BaseModel):
    userQuery: str = Field(..., description="The natural language question or prompt from the user.")
    chapterId: str = Field(..., description="Identifier of the book chapter from which the query originated.")
    sessionId: str = Field(..., description="Identifier of the current chat session.")
    userId: str = Field("anonymous", description="Identifier of the interacting user.")
    selectedText: Optional[str] = Field(None, description="Optional text segment highlighted by the user from the frontend.")
    lastModelMessages: Optional[List[Dict[str, str]]] = Field(None, description="The last few messages from the AI assistant in the current session, for context.")

class AgentMetadataResponse(BaseModel):
    chapters: List[Dict[str, str]]
    sections: List[Dict[str, str]]
    bookMetadata: Dict[str, str]

@router.post("/agent/query")
async def stream_agent_query(request: Request, query_request: AgentQueryRequest):
    """
    Streams AI Assistant responses for a given query using Server-Sent Events (SSE).
    """
    
    # In a real application, you'd perform authentication/authorization here
    # and potentially use the request.client.host for rate limiting.
    
    async def event_generator():
        try:
            async for chunk in agent_service.process_agent_stream(
                user_query=query_request.userQuery,
                chapter_id=query_request.chapterId,
                session_id=query_request.sessionId,
                user_id=query_request.userId,
                selected_text=query_request.selectedText,
                last_model_messages=query_request.lastModelMessages
            ):
                # Format chunk as SSE
                yield f"data: {json.dumps({'token': chunk})}\\n\n"
            
            # Send a final event to indicate stream completion
            yield f"data: {json.dumps({'event': 'end', 'token': ''})}\\n\n"
        except asyncio.CancelledError:
            print("Client disconnected, stream cancelled.")
        except Exception as e:
            print(f"Error in streaming: {e}")
            yield f"data: {json.dumps({'error': str(e), 'event': 'error'})}\\n\n"

    # Need to handle application/json vs text/event-stream based on Accept header
    # For simplicity, always return SSE for now as per spec
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/agent/metadata")
async def get_agent_metadata():
    """
    Returns lists of chapters, sections, and general book metadata for UI use.
    This is a placeholder and would typically query a database or metadata service.
    """
    # This data would come from the ChapterMetadataTool or a dedicated service
    # For now, providing mock data
    mock_chapters = [
        {"id": "module-1-ros2-basics", "title": "ROS 2 Basics"},
        {"id": "module-2-digital-twin", "title": "Digital Twin Concepts"}
    ]
    mock_sections = [
        {"id": "section-1", "title": "Introduction"},
        {"id": "section-2", "title": "Setup"}
    ]
    mock_book_metadata = {
        "title": "Physical AI & Humanoid Robotics",
        "author": "AI Agent",
        "version": "1.0"
    }

    return JSONResponse(
        content=AgentMetadataResponse(
            chapters=mock_chapters,
            sections=mock_sections,
            bookMetadata=mock_book_metadata
        ).dict()
    )

# To integrate these routes into the main FastAPI application (backend/src/main.py),
# you would add: `app.include_router(agent_router.router, prefix="/api")`
# and `app.add_middleware(AgentSecurityMiddleware)`
