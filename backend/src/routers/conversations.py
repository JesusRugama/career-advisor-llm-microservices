from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from xai_client import get_career_advice
from user_profile.user_profile import HARDCODED_USER_PROFILE
from database import get_db
from models.conversation import Conversation
from models.message import Message
from models.user import User

router = APIRouter()

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

@router.get("/users/{user_id}/conversation/{conversation_id}/history")
async def get_conversation_history(
    user_id: UUID,
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> ConversationResponse:
    """Get history for a specific conversation"""
    try:
        # Get the specific conversation
        conv_result = await db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        )
        conversation = conv_result.scalars().first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get messages for this conversation
        messages_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        messages = messages_result.scalars().all()
        
        message_responses = [
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at.isoformat(),
                conversation_id=msg.conversation_id
            )
            for msg in messages
        ]
        
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at.isoformat(),
            messages=message_responses
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")

@router.post("/users/{user_id}/conversation/{conversation_id}/message")
async def post_conversation_message(
    user_id: UUID,
    conversation_id: UUID,
    request: MessageRequest,
    db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    """Send a message to a specific conversation"""
    try:
        # Verify conversation exists and belongs to user
        conv_result = await db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        )
        conversation = conv_result.scalars().first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        
        # Get AI response
        ai_response = await get_career_advice(HARDCODED_USER_PROFILE, request.message)
        
        # Save AI message
        ai_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response.get("response", "Sorry, I couldn't generate a response.")
        )
        db.add(ai_message)
        
        await db.commit()
        
        return MessageResponse(
            id=ai_message.id,
            role=ai_message.role,
            content=ai_message.content,
            created_at=ai_message.created_at.isoformat(),
            conversation_id=ai_message.conversation_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
