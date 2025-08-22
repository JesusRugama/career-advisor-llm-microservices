from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class MessageRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: str
    conversation_id: UUID

class ConversationResponse(BaseModel):
    id: UUID
    title: str
    created_at: str
    messages: List[MessageResponse]
