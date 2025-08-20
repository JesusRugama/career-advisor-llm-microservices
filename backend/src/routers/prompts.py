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
    prompts = [
        {
            'id': uuid.uuid4(),
            'title': 'Career Path Guidance',
            'prompt': 'What are the best career paths for someone with my skills and experience?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Skill Development',
            'prompt': 'What skills should I focus on developing next to advance my career?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Leadership Transition',
            'prompt': 'How can I transition from an individual contributor to a technical leadership role?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Industry Trends',
            'prompt': 'What are the current trends in software engineering that I should be aware of?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Salary Negotiation',
            'prompt': 'How can I effectively negotiate my salary and compensation package?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Work-Life Balance',
            'prompt': 'How can I maintain a healthy work-life balance while advancing my career?'
        }
    ]

    return PromptList(
        success=True,
        prompts=prompts
    )