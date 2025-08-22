from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID

class ConversationBase(BaseModel):
    id: UUID
    title: str
    created_at: str
    model_config = ConfigDict(from_attributes=True)

class ConversationListResponse(BaseModel):
    success: bool
    conversations: List[ConversationBase]
