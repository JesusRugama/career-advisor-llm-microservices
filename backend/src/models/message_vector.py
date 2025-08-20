from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from .base import BaseModel

class MessageVector(BaseModel):
    __tablename__ = "message_vectors"
    
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False)
    vector = Column(Vector(1536))  # OpenAI embedding dimension
    
    # Relationships
    message = relationship("Message", back_populates="vector")
