import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../shared'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from fastapi import Depends

from database import get_db
from models import Conversation

class ConversationRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def get_conversations_by_user_id(self, user_id: UUID) -> List[Conversation]:
        """Get all conversations for a specific user."""
        result = await self.db.scalars(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
        )
        return list(result)
    
    async def get_conversation_by_id(self, conversation_id: UUID, user_id: UUID) -> Conversation | None:
        """Get a specific conversation by ID and user ID."""
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        )
        return result.scalars().first()
