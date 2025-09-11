import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../shared'))

from sqlalchemy import Column, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from base import BaseModel

class Message(BaseModel):
    __tablename__ = "messages"
    
    conversation_id = Column(UUID(as_uuid=True), nullable=False)  # No foreign key for microservices
    is_human = Column(Boolean, nullable=False)  # True for user, False for assistant
    content = Column(Text, nullable=False)
