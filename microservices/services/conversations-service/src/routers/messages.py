from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from schemas import MessageListResponse, MessageBase, CreateMessageRequest, MessageResponse
from repositories import ConversationRepository, MessageRepository

router = APIRouter()

@router.get("/users/{user_id}/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    user_id: UUID,
    conversation_id: UUID,
    conversation_repository: ConversationRepository = Depends(),
    message_repository: MessageRepository = Depends()
) -> MessageListResponse:
    """
    Get all messages for a specific conversation
    """
    try:
        # Verify conversation exists and belongs to user
        conversation_exists = await conversation_repository.conversation_exists(conversation_id, user_id)

        if not conversation_exists:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = await message_repository.get_messages_by_conversation_id(conversation_id)

        return MessageListResponse(
            success=True,
            messages=[MessageBase.model_validate(msg) for msg in messages]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation messages: {str(e)}")

@router.post("/users/{user_id}/conversations/{conversation_id}/message")
async def create_conversation_message(
    user_id: UUID,
    conversation_id: UUID,
    request: CreateMessageRequest,
    conversation_repository: ConversationRepository = Depends(),
    message_repository: MessageRepository = Depends()
) -> MessageResponse:
    """Send a message to a specific conversation"""
    try:
        # Verify conversation exists and belongs to user
        conversation_exists = await conversation_repository.conversation_exists(conversation_id, user_id)
        
        if not conversation_exists:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Save user message
        user_message = await message_repository.create_message(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        
        return MessageResponse(
            success=True,
            message=MessageBase.model_validate(user_message)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
        