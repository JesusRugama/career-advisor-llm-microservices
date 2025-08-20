from fastapi import APIRouter

from pydantic import BaseModel
from uuid import UUID
from typing import List
import uuid

router = APIRouter()

class PromptResponse(BaseModel):
    id: UUID
    title: str
    prompt: str

class PromptList(BaseModel):
    success: bool
    prompts: List[PromptResponse]

@router.get("/prompts")
def get_predefined_prompts() -> PromptList:
    """
    Get predefined career advice prompts to help users get started
    """


    return PromptList(
        success=True,
        prompts=prompts
    )