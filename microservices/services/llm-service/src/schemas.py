from pydantic import BaseModel
from typing import Dict, Any, Optional


class CareerAdviceRequest(BaseModel):
    """Request schema for career advice"""

    user_profile: Dict[str, Any]
    question: Optional[str] = None


class CareerAdviceResponse(BaseModel):
    """Response schema for career advice"""

    success: bool
    response: str
    error: Optional[str] = None
