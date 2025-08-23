from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from user_profile.user_profile import HARDCODED_USER_PROFILE
from shared.ai_client import AIServiceClient
from .schemas import MessageRequest, MessageResponse, ConversationResponse
from .repository import MessageRepository

router = APIRouter()

@router.get("/users/{user_id}/conversations/{conversation_id}/history")
async def get_conversation_history(
    user_id: UUID,
    conversation_id: UUID,
    repository: MessageRepository = Depends()
) -> ConversationResponse:
    """
    Get history for a specific conversation
    """
    try:
        conversation, messages = await repository.get_conversation_with_messages(conversation_id, user_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        message_responses = [MessageResponse.model_validate(msg) for msg in messages]
        
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            messages=message_responses
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")

@router.post("/users/{user_id}/conversations/{conversation_id}/message")
async def post_conversation_message(
    user_id: UUID,
    conversation_id: UUID,
    request: MessageRequest,
    repository: MessageRepository = Depends()
) -> MessageResponse:
    """Send a message to a specific conversation"""
    try:
        # Verify conversation exists and belongs to user
        conversation, _ = await repository.get_conversation_with_messages(conversation_id, user_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Save user message
        user_message = await repository.create_message(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        
        # Get AI response using the AI service client
        ai_client = AIServiceClient()
        ai_response = await ai_client.get_career_advice(HARDCODED_USER_PROFILE, request.message)
        
        # Save AI message
        ai_message = await repository.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response.get("response", "Sorry, I couldn't generate a response.")
        )
        
        await repository.db.commit()
        
        return MessageResponse.model_validate(ai_message)
        
    except HTTPException:
        raise
    except Exception as e:
        await repository.db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
