import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../shared"))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from fastapi import Depends

from database import get_db
from models.messages import Message


class MessageRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_messages_by_conversation_id(
        self, conversation_id: UUID
    ) -> List[Message]:
        """Get all messages for a specific conversation."""
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()

    async def create_message(
        self, conversation_id: UUID, is_human: bool, content: str
    ) -> Message:
        """Create a new message."""
        message = Message(
            conversation_id=conversation_id, is_human=is_human, content=content
        )
        self.db.add(message)
        await self.db.flush()  # Get the ID without committing
        return message
