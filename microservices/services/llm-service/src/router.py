from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from schemas import CareerAdviceRequest, CareerAdviceResponse
from service import AIService

router = APIRouter()

@router.post("/ai/career-advice")
async def get_career_advice(
    request: CareerAdviceRequest
) -> CareerAdviceResponse:
    """
    Get AI-powered career advice based on user profile and optional question
    """
    try:
        ai_service = AIService()
        result = await ai_service.get_career_advice(
            user_profile=request.user_profile,
            question=request.question
        )
        
        return CareerAdviceResponse(
            success=result["success"],
            response=result["response"],
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error getting career advice: {str(e)}"
        )
