import sys
import os

# Add shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../shared"))
# Add current directory to path for local imports
sys.path.append(os.path.dirname(__file__))

from fastapi import APIRouter, Depends, HTTPException, Request
from uuid import UUID
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from schemas import (
    MessageListResponse,
    MessageBase,
    CreateMessageRequest,
    MessageResponse,
    MessageWithConversationResponse,
    ConversationBase,
)
from repositories import ConversationRepository, MessageRepository
from services.ai_service import AIService
from feign_clients.users_client import UsersClient

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.get("/users/{user_id}/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    user_id: UUID,
    conversation_id: UUID,
    conversation_repository: ConversationRepository = Depends(),
    message_repository: MessageRepository = Depends(),
) -> MessageListResponse:
    """
    Get all messages for a specific conversation
    """
    try:
        # Verify conversation exists and belongs to user
        conversation_exists = await conversation_repository.conversation_exists(
            conversation_id, user_id
        )

        if not conversation_exists:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = await message_repository.get_messages_by_conversation_id(
            conversation_id
        )

        return MessageListResponse(
            success=True, messages=[MessageBase.model_validate(msg) for msg in messages]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving conversation messages: {str(e)}"
        )


@router.post("/users/{user_id}/conversations/{conversation_id}/message")
@limiter.limit("10/minute")
async def create_conversation_message(
    request: Request,
    user_id: UUID,
    conversation_id: UUID,
    message_request: CreateMessageRequest,
    conversation_repository: ConversationRepository = Depends(),
    message_repository: MessageRepository = Depends(),
) -> MessageResponse:
    """Send a message to a specific conversation and get AI career advice"""
    try:
        # Verify conversation exists and belongs to user
        conversation_exists = await conversation_repository.conversation_exists(
            conversation_id, user_id
        )

        if not conversation_exists:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Save user message
        user_message = await message_repository.create_message(
            conversation_id=conversation_id, is_human=True, content=message_request.message
        )

        # Commit the user message first
        await message_repository.db.commit()
        await message_repository.db.refresh(user_message)

        # Get user profile from Users Service
        users_client = UsersClient()
        user_profile = await users_client.get_user_profile(user_id)

        if not user_profile:
            raise HTTPException(
                status_code=404,
                detail="User profile not found. Please complete your profile first.",
            )

        # Get AI career advice
        ai_service = AIService()
        ai_response = await ai_service.get_career_advice(
            user_profile=user_profile, question=message_request.message
        )

        # Save AI response as assistant message
        if ai_response.get("success", False):
            ai_message = await message_repository.create_message(
                conversation_id=conversation_id,
                is_human=False,
                content=ai_response["response"],
            )

            # Commit the AI message
            await message_repository.db.commit()
            await message_repository.db.refresh(ai_message)

            # Return the AI response message
            return MessageResponse(
                success=True, message=MessageBase.model_validate(ai_message)
            )
        else:
            # If AI service failed, return error message
            error_message = await message_repository.create_message(
                conversation_id=conversation_id,
                is_human=False,
                content="I apologize, but I'm having trouble generating a response right now. Please try again later.",
            )

            await message_repository.db.commit()
            await message_repository.db.refresh(error_message)

            return MessageResponse(
                success=False, message=MessageBase.model_validate(error_message)
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing message: {str(e)}"
        )


@router.post("/users/{user_id}/messages")
@limiter.limit("10/minute")
async def create_conversation_and_message(
    request: Request,
    user_id: UUID,
    message_request: CreateMessageRequest,
    message_repository: MessageRepository = Depends(),
    conversation_repository: ConversationRepository = Depends(),
) -> MessageWithConversationResponse:
    """Create a new conversation with the first message"""
    try:
        # Always create new conversation
        conversation = await conversation_repository.create_conversation(
            user_id, "New Conversation"
        )

        # Create the message
        message = await message_repository.create_message(
            conversation_id=conversation.id, is_human=True, content=message_request.message
        )

        # Commit the transaction first
        await message_repository.db.commit()

        # Refresh objects to load all attributes after commit
        await message_repository.db.refresh(message)
        await conversation_repository.db.refresh(conversation)

        return MessageWithConversationResponse(
            success=True,
            message=MessageBase.model_validate(message),
            conversation=ConversationBase.model_validate(conversation).model_dump(),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")
