import httpx
from typing import Dict, Any, Optional
from fastapi import HTTPException

from config import settings


class AIServiceClient:
    """HTTP client for communicating with the AI service"""

    def __init__(self):
        # For now, we'll use internal service calls since it's the same app
        # In a true microservices setup, this would be a different service URL
        self.base_url = getattr(settings, "ai_service_url", "http://localhost:8000")
        self.timeout = 30.0

    async def get_career_advice(
        self, user_profile: Dict[str, Any], question: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get career advice from the AI service via HTTP request
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/ai/career-advice",
                    json={"user_profile": user_profile, "question": question},
                    headers={"Content-Type": "application/json"},
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"AI service error: {response.text}",
                    )

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504, detail="AI service timeout - please try again"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"AI service unavailable: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error communicating with AI service: {str(e)}"
            )
