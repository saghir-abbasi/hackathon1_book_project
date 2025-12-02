from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any, Optional
from ..models.chat_models import ChatRequest, ChatResponse, ChatMessage
from ..services.rag_service import retrieve_relevant_segments, generate_rag_response
from ..config import settings
from ..db.database import get_db, create_session, get_session, add_chat_message # Import DB functions
from sqlalchemy.orm import Session # Import Session for dependency
import uuid
import datetime
import json # For serializing context_used to JSON string

router = APIRouter()

@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_rag_chatbot(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Accepts user input, retrieves relevant context, and returns an assistant response.
    Manages chat sessions and can store conversation history.
    """
    try:
        current_session_id = request.session_id
        user_session = None

        if current_session_id:
            # Attempt to retrieve existing session
            user_session = get_session(db, current_session_id)
            if not user_session:
                # If session_id is provided but not found, create a new one.
                user_session = create_session(db)
                current_session_id = user_session.session_id
        else:
            # Create a new session if no session_id is provided
            user_session = create_session(db)
            current_session_id = user_session.session_id
        
        # --- RAG Pipeline ---
        # 1. Retrieve relevant segments based on user's message
        relevant_segments = await retrieve_relevant_segments(request.user_message)
        context_used = [seg["text"] for seg in relevant_segments]

        # 2. Generate RAG response using the context
        assistant_response_text = await generate_rag_response(request.user_message, relevant_segments)

        # --- Session Management ---
        # Add user's message to history
        add_chat_message(
            db=db,
            session_id=current_session_id,
            sender="user",
            text=request.user_message,
            context_retrieved_json=None # Context is for bot's response
        )
        # Add assistant's message to history
        new_assistant_message = add_chat_message(
            db=db,
            session_id=current_session_id,
            sender="bot",
            text=assistant_response_text,
            context_retrieved_json=json.dumps(context_used) if context_used else None
        )
        
        return ChatResponse(
            session_id=current_session_id,
            assistant_response=assistant_response_text,
            chat_message_id=new_assistant_message.message_id,
            context_used=context_used
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )