from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from .base import BaseModel

class Conversation(BaseModel):
    __tablename__ = "conversations"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    summary = relationship("ConversationSummary", back_populates="conversation", uselist=False)

class ConversationSummary(BaseModel):
    __tablename__ = "conversation_summaries"
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    summary_text = Column(Text, nullable=False)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="summary")

class Message(BaseModel):
    __tablename__ = "messages"
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    prompt = relationship("Prompt")
    vector = relationship("MessageVector", back_populates="message", uselist=False)

class MessageVector(BaseModel):
    __tablename__ = "message_vectors"
    
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False)
    vector = Column(Vector(1536))  # OpenAI embedding dimension
    
    # Relationships
    message = relationship("Message", back_populates="vector")
