from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import BaseModel

class Conversation(BaseModel):
    __tablename__ = "conversations"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    summary = relationship("ConversationSummary", back_populates="conversation", uselist=False)
