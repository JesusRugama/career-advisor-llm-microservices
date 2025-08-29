from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID

from schemas import ConversationListResponse, ConversationBase, CreateConversationRequest, ConversationResponse
from repository import ConversationRepository

router = APIRouter()

@router.get("/users/{user_id}/conversations")
async def get_conversations(
        user_id: UUID,
        repository: ConversationRepository = Depends()
) -> ConversationListResponse:
    """
    Get conversations for a specific user
    """
    try:
        conversations = await repository.get_conversations(user_id)

        return ConversationListResponse(
            success=True,
            conversations=[ConversationBase.model_validate(conv) for conv in conversations]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/users/{user_id}/conversations/{conversation_id}")
# async def get_conversation(
#         conversation_id: UUID,
#         user_id: UUID = Query(..., description="User ID to verify ownership"),
#         repository: ConversationRepository = Depends()
# ) -> ConversationResponse:
#     """
#     Get a specific conversation by ID and verify it belongs to the user
#     """
#     try:
#         conversation = await repository.get_conversation_by_id(conversation_id, user_id)
#
#         if not conversation:
#             raise HTTPException(status_code=404, detail="Conversation not found")
#
#         return ConversationResponse(
#             success=True,
#             conversation=ConversationBase.model_validate(conversation)
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @router.post("/users/{user_id}/conversations", status_code=201)
# async def create_conversation(
#         request: CreateConversationRequest,
#         repository: ConversationRepository = Depends()
# ) -> ConversationResponse:
#     """
#     Create a new conversation for a user
#     """
#     try:
#         conversation = await repository.create_conversation(request.user_id, request.title)
#
#         return ConversationResponse(
#             success=True,
#             conversation=ConversationBase.model_validate(conversation)
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
