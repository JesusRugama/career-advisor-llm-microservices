from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class CreateMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class MessageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    role: str
    content: str
    created_at: datetime
    conversation_id: UUID


class MessageListResponse(BaseModel):
    success: bool
    messages: List[MessageBase]

class MessageResponse(BaseModel):
    success: bool
    message: MessageBase

