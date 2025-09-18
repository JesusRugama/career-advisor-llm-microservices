from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from schemas import UserProfileResponse, UserProfileBase
from repository import UserRepository

router = APIRouter()


@router.get("/users/{user_id}/profile")
async def get_user_profile(
    user_id: UUID, repository: UserRepository = Depends()
) -> UserProfileResponse:
    """Get user profile by user ID."""
    try:
        # First check if user exists
        user = await repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get user profile
        profile = await repository.get_user_profile(user_id)
        if not profile:
            return UserProfileResponse(
                success=True, profile=None, message="User profile not found"
            )

        profile_data = UserProfileBase.model_validate(profile)
        return UserProfileResponse(success=True, profile=profile_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
