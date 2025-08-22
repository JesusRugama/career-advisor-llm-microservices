from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID

class PromptBase(BaseModel):
    id: UUID
    title: str
    prompt_text: str
    model_config = ConfigDict(from_attributes=True)

class PromptListResponse(BaseModel):
    success: bool
    prompts: List[PromptBase]
