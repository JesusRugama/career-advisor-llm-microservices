import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../shared"))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from fastapi import Depends

from database import get_db
from models import User, UserProfile


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get a user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_profile(self, user_id: UUID) -> UserProfile | None:
        """Get user profile by user ID."""
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalars().first()
