from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from .models import Prompt
from .schemas import PromptBase

class PromptService:
    """Service class for prompt-related business logic."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_active_prompts(self) -> List[PromptBase]:
        """Get all active prompts from the database."""
        prompts = await self.db.scalars(
            select(Prompt).where(Prompt.is_active == True)
        )
        return [PromptBase.model_validate(prompt) for prompt in prompts]
