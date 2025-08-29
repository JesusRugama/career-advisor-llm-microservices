import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../shared'))

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from base import BaseModel

class Conversation(BaseModel):
    __tablename__ = "conversations"
    
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(255), nullable=False)
