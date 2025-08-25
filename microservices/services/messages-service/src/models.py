import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from base import BaseModel

class Message(BaseModel):
    __tablename__ = "messages"
    
    conversation_id = Column(UUID(as_uuid=True), nullable=False)  # No foreign key for microservices
    role = Column(String(50), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    
    # Relationships removed for microservices independence

class MessageVector(BaseModel):
    __tablename__ = "message_vectors"
    
    message_id = Column(UUID(as_uuid=True), nullable=False)  # No foreign key for microservices
    vector = Column(Vector(1536))  # OpenAI embedding dimension
