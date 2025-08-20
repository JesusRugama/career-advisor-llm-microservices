from sqlalchemy import Column, String, Text, Boolean
from .base import BaseModel

class Prompt(BaseModel):
    __tablename__ = "prompts"
    
    title = Column(String(255), nullable=False)
    prompt_text = Column(Text, nullable=False)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
