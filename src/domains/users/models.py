from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    conversations = relationship("Conversation", back_populates="user")
