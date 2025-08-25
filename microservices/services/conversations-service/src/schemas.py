from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID
from datetime import datetime

class ConversationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    created_at: datetime
    user_id: UUID

class ConversationListResponse(BaseModel):
    success: bool
    conversations: List[ConversationBase]

class CreateConversationRequest(BaseModel):
    user_id: UUID
    title: str

class ConversationResponse(BaseModel):
    success: bool
    conversation: ConversationBase
