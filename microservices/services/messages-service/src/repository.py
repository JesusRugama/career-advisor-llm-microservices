import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../shared'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from fastapi import Depends

from database import get_db
from models import Message
from domains.conversations.models import Conversation

class MessageRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def get_messages_by_conversation_id(self, conversation_id: UUID) -> List[Message]:
        """Get all messages for a specific conversation."""
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()
    
    async def create_message(self, conversation_id: UUID, role: str, content: str) -> Message:
        """Create a new message."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        self.db.add(message)
        await self.db.flush()  # Get the ID without committing
        return message
    
    async def get_conversation_with_messages(self, conversation_id: UUID, user_id: UUID) -> List[Message]:
        """Get conversation and its messages."""
        # Get conversation
        # conv_result = await self.db.execute(
        #     select(Conversation)
        #     .where(Conversation.id == conversation_id)
        #     .where(Conversation.user_id == user_id)
        # )
        # conversation = conv_result.scalars().first()
        #
        # if not conversation:
        #     return None, []
        
        # Get messages
        messages = await self.get_messages_by_conversation_id(conversation_id)
        return messages
