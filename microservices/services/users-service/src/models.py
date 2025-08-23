import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    
    # Relationships - Note: In microservices, these will be handled via HTTP calls
    # profile = relationship("UserProfile", back_populates="user", uselist=False)
    # conversations = relationship("Conversation", back_populates="user")
