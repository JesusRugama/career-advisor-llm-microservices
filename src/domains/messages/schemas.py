from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class MessageRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    role: str
    content: str
    created_at: datetime
    conversation_id: UUID

class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    created_at: datetime
    messages: List[MessageResponse]
