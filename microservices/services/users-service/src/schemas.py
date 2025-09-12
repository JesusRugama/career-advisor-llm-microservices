from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List, Any


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str


class UserProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    years_experience: Optional[int] = None
    skills: Optional[List[str]] = None
    career_goals: Optional[str] = None
    preferred_work_style: Optional[str] = None


class UserProfileResponse(BaseModel):
    success: bool
    profile: Optional[UserProfileBase] = None
    message: Optional[str] = None
