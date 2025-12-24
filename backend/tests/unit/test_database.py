from src.db.database import SessionLocal, engine, create_session, get_session, add_chat_message, get_chat_history
from src.db.base_class import Base # Import Base from its new location
from src.models.db_models import UserSession, ChatMessage
import pytest
from sqlalchemy.orm import Session
import uuid
import datetime
import json

# Setup and Teardown for tests
@pytest.fixture(name="db_session")
def db_session_fixture():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after tests, in reverse order of creation
        Base.metadata.drop_all(bind=engine)

def test_create_session(db_session: Session):
    """Test creating a new user session."""
    session = create_session(db_session)
    assert session is not None
    assert session.session_id is not None
    assert session.user_id is None
    assert session.start_time is not None
    assert session.last_active_time is not None

    retrieved_session = get_session(db_session, session.session_id)
    assert retrieved_session == session

def test_create_session_with_user_id(db_session: Session):
    """Test creating a new user session with a specified user ID."""
    test_user_id = "test_user_123"
    session = create_session(db_session, user_id=test_user_id)
    assert session.user_id == test_user_id

    retrieved_session = get_session(db_session, session.session_id)
    assert retrieved_session.user_id == test_user_id

def test_get_non_existent_session(db_session: Session):
    """Test retrieving a session that does not exist."""
    non_existent_uuid = uuid.uuid4()
    session = get_session(db_session, non_existent_uuid)
    assert session is None

def test_add_chat_message(db_session: Session):
    """Test adding a chat message to a session."""
    session = create_session(db_session)
    message_text = "Hello, chatbot!"
    sender = "user"
    context = {"source": "book_intro"}
    
    message = add_chat_message(db_session, session.session_id, sender, message_text, json.dumps(context))
    
    assert message is not None
    assert message.message_id is not None
    assert message.session_id == session.session_id
    assert message.sender == sender
    assert message.text == message_text
    assert message.timestamp is not None
    assert json.loads(message.context_retrieved_json) == context

    history = get_chat_history(db_session, session.session_id)
    assert len(history) == 1
    assert history[0] == message

def test_get_chat_history(db_session: Session):
    """Test retrieving multiple chat messages for a session."""
    session = create_session(db_session)
    
    msg1 = add_chat_message(db_session, session.session_id, "user", "Hi", None)
    msg2 = add_chat_message(db_session, session.session_id, "bot", "Hello", json.dumps({"qdrant_hits": 1}))
    msg3 = add_chat_message(db_session, session.session_id, "user", "How are you?", None)

    history = get_chat_history(db_session, session.session_id)
    assert len(history) == 3
    assert history[0].text == "Hi"
    assert history[1].text == "Hello"
    assert history[2].text == "How are you?"
    # Check ordering by timestamp
    assert history[0].timestamp <= history[1].timestamp <= history[2].timestamp

def test_update_session_last_active(db_session: Session):
    """Test updating the last active time of a session."""
    session = create_session(db_session)
    original_last_active = session.last_active_time
    
    # Simulate some delay or activity
    import time
    time.sleep(0.1) 

    updated_session = db_session.query(UserSession).filter(UserSession.session_id == session.session_id).first()
    updated_session.last_active_time = datetime.datetime.utcnow()
    db_session.add(updated_session)
    db_session.commit()
    db_session.refresh(updated_session)
    
    assert updated_session.last_active_time > original_last_active
