import sys
import os

# Add shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../shared"))
# Add current directory to path for local imports
sys.path.append(os.path.dirname(__file__))

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

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
from dependencies import get_users_client, get_ai_service

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
async def create_conversation_message(
    user_id: UUID,
    conversation_id: UUID,
    message_request: CreateMessageRequest,
    conversation_repository: ConversationRepository = Depends(),
    message_repository: MessageRepository = Depends(),
    users_client: UsersClient = Depends(get_users_client),
    ai_service: AIService = Depends(get_ai_service),
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
            conversation_id=conversation_id,
            is_human=True,
            content=message_request.message,
        )

        # Commit the user message first
        await message_repository.db.commit()
        await message_repository.db.refresh(user_message)

        # Get user profile from Users Service
        user_profile = await users_client.get_user_profile(user_id)

        if not user_profile:
            raise HTTPException(
                status_code=404,
                detail="User profile not found. Please complete your profile first.",
            )

        # Get AI career advice
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
async def create_conversation_and_message(
    user_id: UUID,
    message_request: CreateMessageRequest,
    conversation_repository: ConversationRepository = Depends(),
    message_repository: MessageRepository = Depends(),
    users_client: UsersClient = Depends(get_users_client),
    ai_service: AIService = Depends(get_ai_service),
) -> MessageWithConversationResponse:
    """Create a new conversation with the first message and get AI response"""
    try:
        # Always create new conversation
        conversation = await conversation_repository.create_conversation(
            user_id, "New Conversation"
        )

        # Commit the conversation first
        await conversation_repository.db.commit()
        await conversation_repository.db.refresh(conversation)

        # Use the existing create_conversation_message logic
        message_response = await create_conversation_message(
            user_id=user_id,
            conversation_id=conversation.id,
            message_request=message_request,
            conversation_repository=conversation_repository,
            message_repository=message_repository,
            users_client=users_client,
            ai_service=ai_service,
        )

        # Return both the conversation and the AI message
        return MessageWithConversationResponse(
            success=message_response.success,
            message=message_response.message,
            conversation=ConversationBase.model_validate(conversation).model_dump(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating conversation and message: {str(e)}")
