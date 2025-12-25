from sqlalchemy import create_engine # Import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.base_class import Base # Import Base from the new module
from ..config import settings
from ..models.db_models import UserSession, ChatMessage # Import models
import os
import uuid
import datetime
from typing import Generator, Optional, List, Dict, Any


# Database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """
    Creates database tables defined by Base metadata.
    This is an additive-only operation; it will not modify existing data.
    """
    # Import models here to ensure they are registered with Base
    from ..models import db_models # pylint: disable=unused-import, import-outside-toplevel
    from ..auth import models as auth_models # pylint: disable=unused-import, import-outside-toplevel
    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if they didn't exist).")

# --- Helper functions for session data ---

def get_session(db: SessionLocal, session_id: uuid.UUID) -> Optional[UserSession]:
    """Retrieves a user session by its ID."""
    return db.query(UserSession).filter(UserSession.session_id == session_id).first()

def create_session(db: SessionLocal, user_id: Optional[str] = None) -> UserSession:
    """Creates a new user session."""
    new_session = UserSession(user_id=user_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def update_session_last_active(db: SessionLocal, session: UserSession) -> UserSession:
    """Updates the last active time of a session."""
    session.last_active_time = datetime.datetime.utcnow()
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def add_chat_message(
    db: SessionLocal,
    session_id: uuid.UUID,
    sender: str,
    text: str,
    context_retrieved_json: Optional[str] = None
) -> ChatMessage:
    """Adds a new chat message to a session."""
    new_message = ChatMessage(
        session_id=session_id,
        sender=sender,
        text=text,
        context_retrieved_json=context_retrieved_json
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_chat_history(db: SessionLocal, session_id: uuid.UUID) -> List[ChatMessage]:
    """Retrieves chat history for a given session."""
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.timestamp).all()
