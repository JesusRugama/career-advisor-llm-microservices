from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class MessageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    is_human: bool
    content: str
    created_at: datetime
    conversation_id: UUID

class MessageListResponse(BaseModel):
    success: bool
    messages: List[MessageBase]

class CreateMessageRequest(BaseModel):
    message: str

class CreateMessageWithConversationRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class MessageResponse(BaseModel):
    success: bool
    message: MessageBase

class MessageWithConversationResponse(BaseModel):
    success: bool
    message: MessageBase
    conversation: dict  # Will contain conversation details if newly created
