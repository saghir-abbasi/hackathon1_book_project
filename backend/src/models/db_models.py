from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.base_class import Base
import datetime
import uuid

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    last_active_time = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = Column(String, nullable=True) # Can be null if no auth
    metadata_json = Column(String, nullable=True) # Store as JSON string
    
    chat_messages = relationship("ChatMessage", back_populates="session", lazy="joined")

    def __repr__(self):
        return f"<UserSession(session_id='{self.session_id}', user_id='{self.user_id}', start_time='{self.start_time}')>"

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("user_sessions.session_id"))
    sender = Column(String, nullable=False) # "user" or "bot"
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    context_retrieved_json = Column(String, nullable=True) # Store as JSON string

    session = relationship("UserSession", back_populates="chat_messages")

    def __repr__(self):
        return f"<ChatMessage(message_id='{self.message_id}', session_id='{self.session_id}', sender='{self.sender}')>"
