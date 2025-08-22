from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from .models import User
from .schemas import UserListResponse, UserResponse, UserBase
from .repository import UserRepository

router = APIRouter()

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)) -> UserListResponse:
    """Get all users from the database."""
    try:
        repository = UserRepository(db)
        users = await repository.get_all_users()
        
        user_responses = [
            UserBase(
                id=user.id,
                name=user.name,
                email=user.email
            )
            for user in users
        ]
        
        return UserListResponse(
            success=True,
            users=user_responses
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users")
async def create_user(db: AsyncSession = Depends(get_db)) -> UserResponse:
    """Create a new user."""
    return UserResponse(
        success=True,
        message="User creation endpoint - implementation needed"
    )
