from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from schemas import MessageListResponse, MessageBase, CreateMessageRequest, MessageResponse, MessageWithConversationResponse, ConversationBase
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

@router.post("/users/{user_id}/messages")
async def create_conversation_and_message(
    user_id: UUID,
    request: CreateMessageRequest,
    message_repository: MessageRepository = Depends(),
    conversation_repository: ConversationRepository = Depends()
) -> MessageWithConversationResponse:
    """Create a new conversation with the first message"""
    try:
        # Always create new conversation
        conversation = await conversation_repository.create_conversation(user_id, "New Conversation")
        
        # Create the message
        message = await message_repository.create_message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        
        return MessageWithConversationResponse(
            success=True,
            message=MessageBase.model_validate(message),
            conversation=ConversationBase.model_validate(conversation).model_dump()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")
        