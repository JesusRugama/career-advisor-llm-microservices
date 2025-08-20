from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    conversations = relationship("Conversation", back_populates="user")

class UserProfile(BaseModel):
    __tablename__ = "user_profiles"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    years_experience = Column(Integer)
    skills = Column(JSON)  # JSON field for flexible skills storage
    career_goals = Column(Text)
    preferred_work_style = Column(String(50))  # remote, hybrid, onsite
    
    # Relationships
    user = relationship("User", back_populates="profile")
