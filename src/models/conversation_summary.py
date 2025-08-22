from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel

class ConversationSummary(BaseModel):
    __tablename__ = "conversation_summaries"
    
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    summary_text = Column(Text, nullable=False)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="summary")
