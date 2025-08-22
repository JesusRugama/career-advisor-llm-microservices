import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import APIRouter, Depends, HTTPException
from .repository import PromptRepository
from .schemas import PromptListResponse

router = APIRouter()

@router.get("/prompts", response_model=PromptListResponse)
async def get_prompts(service: PromptRepository = Depends(PromptRepository)):
    """
    Get predefined career advice prompts to help users get started
    """
    try:
        prompts = await service.get_active_prompts()
        return PromptListResponse(
            success=True,
            prompts=prompts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
