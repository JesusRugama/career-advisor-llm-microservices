import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .service import PromptService
from .schemas import PromptListResponse

router = APIRouter()

@router.get("/prompts", response_model=PromptListResponse)
async def get_predefined_prompts(db: AsyncSession = Depends(get_db)):
    """
    Get predefined career advice prompts to help users get started
    """
    try:
        service = PromptService(db)
        prompts = await service.get_active_prompts()
        return PromptListResponse(
            success=True,
            prompts=prompts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
