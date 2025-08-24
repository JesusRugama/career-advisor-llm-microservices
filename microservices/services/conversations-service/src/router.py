from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from schemas import ConversationListResponse, ConversationBase
from repository import ConversationRepository

router = APIRouter()

@router.get("/users/{user_id}/conversations")
async def get_conversation_history(
        user_id: UUID,
        repository: ConversationRepository = Depends()
) -> ConversationListResponse:
    """
    Get conversations for a specific user
    """
    try:
        conversations = await repository.get_conversations_by_user_id(user_id)

        return ConversationListResponse(
            success=True,
            conversations=[ConversationBase.model_validate(conv) for conv in conversations]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
