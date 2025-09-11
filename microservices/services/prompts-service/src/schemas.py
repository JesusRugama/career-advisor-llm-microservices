from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID


class PromptBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    prompt_text: str


class PromptListResponse(BaseModel):
    success: bool
    prompts: List[PromptBase]
