from fastapi import APIRouter
from pydantic import BaseModel
from xai_client import get_career_advice
from user_profile.user_profile import HARDCODED_USER_PROFILE

# User profile is now imported from config.user_profile (gitignored for privacy)

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/")
async def post_career_advice_question(request: QuestionRequest):
    result = await get_career_advice(HARDCODED_USER_PROFILE, request.question)
    return result
