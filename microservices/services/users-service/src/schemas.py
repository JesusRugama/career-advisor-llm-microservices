from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str


class UserResponse(BaseModel):
    success: bool
    message: str


class UserListResponse(BaseModel):
    success: bool
    users: list[UserBase]
