from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from uuid import UUID
from sqlalchemy import select
from pydantic import BaseModel, ConfigDict
from typing import List
from models.prompt import Prompt

router = APIRouter()

class PromptBase(BaseModel):
    id: UUID
    title: str
    prompt_text: str
    model_config = ConfigDict(from_attributes=True)

class PromptListResponse(BaseModel):
    success: bool
    prompts: List[PromptBase]

@router.get("/prompts", response_model=PromptListResponse)
async def get_predefined_prompts(db: AsyncSession = Depends(get_db)):
    """
    Get predefined career advice prompts to help users get started
    """

    try:
        prompts = await db.scalars(select(Prompt).where(Prompt.is_active == True))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PromptListResponse(
        success=True,
        prompts=list(prompts)
    )
