from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from database import get_db
from models.conversation import Conversation
from models.user import User

router = APIRouter()

class ConversationBase(BaseModel):
    id: UUID
    title: str
    created_at: str
    model_config = ConfigDict(from_attributes=True)

class ConversationListResponse(BaseModel):
    success: bool
    conversations: List[ConversationBase]

@router.get("/users/{user_id}/conversations")
async def get_conversation_history(
        user_id: UUID,
        db: AsyncSession = Depends(get_db)
) -> ConversationListResponse:
    """
    Get conversations for a specific user
    """
    try:
        conversations = await db.scalars(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
        )

        return ConversationListResponse(
            success=True,
            conversations=list(conversations)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
