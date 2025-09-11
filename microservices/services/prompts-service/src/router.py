from fastapi import APIRouter, Depends, HTTPException
from repository import PromptRepository
from schemas import PromptListResponse

router = APIRouter()


@router.get("/prompts", response_model=PromptListResponse)
async def get_prompts(repository: PromptRepository = Depends()):
    """
    Get predefined career advice prompts to help users get started
    """
    try:
        prompts = await repository.get_active_prompts()
        return PromptListResponse(success=True, prompts=prompts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
