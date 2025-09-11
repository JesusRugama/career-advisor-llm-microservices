from fastapi import APIRouter, Depends, HTTPException

from schemas import UserListResponse, UserResponse, UserBase
from repository import UserRepository

router = APIRouter()


@router.get("/users")
async def get_users(repository: UserRepository = Depends()) -> UserListResponse:
    """Get all users from the database."""
    try:
        users = await repository.get_all_users()

        user_responses = [UserBase.model_validate(user) for user in users]

        return UserListResponse(success=True, users=user_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users")
async def create_user(repository: UserRepository = Depends()) -> UserResponse:
    """Create a new user."""
    return UserResponse(
        success=True, message="User creation endpoint - implementation needed"
    )
