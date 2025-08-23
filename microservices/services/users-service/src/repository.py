import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List
from fastapi import Depends

from database import get_db
from models import User

class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def get_all_users(self) -> List[User]:
        """Get all users."""
        result = await self.db.scalars(select(User))
        return list(result)
    
    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get a user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()
    
    async def create_user(self, name: str, email: str) -> User:
        """Create a new user."""
        user = User(name=name, email=email)
        self.db.add(user)
        await self.db.flush()  # Get the ID without committing
        return user
