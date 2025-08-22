from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    id: UUID
    name: str
    email: str

class UserResponse(BaseModel):
    success: bool
    message: str

class UserListResponse(BaseModel):
    success: bool
    users: list[UserBase]
