from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from database import get_db
from .models import Conversation
from .schemas import ConversationListResponse
from .repository import ConversationRepository

router = APIRouter()

@router.get("/users/{user_id}/conversations")
async def get_conversation_history(
        user_id: UUID,
        db: AsyncSession = Depends(get_db)
) -> ConversationListResponse:
    """
    Get conversations for a specific user
    """
    try:
        repository = ConversationRepository(db)
        conversations = await repository.get_conversations_by_user_id(user_id)

        return ConversationListResponse(
            success=True,
            conversations=conversations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
