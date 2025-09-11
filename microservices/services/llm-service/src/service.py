from openai import OpenAI
from typing import Dict, Any, Optional

from config import settings


class AIService:
    """Service class for handling AI-powered career advice requests"""

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.xai_api_key,
            base_url=settings.xai_base_url,
        )

    async def get_career_advice(
        self, user_profile: Dict[str, Any], question: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get career advice from AI based on user profile and optional question"""
        try:
            # Build the prompt
            prompt = self._build_career_prompt(user_profile, question)

            print("AI Service - prompt: ", prompt)
            print("AI Service - api_key: ", settings.xai_api_key)

            # Make the AI request
            response = self.client.chat.completions.create(
                model=settings.xai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a career advisor for software engineers. Provide personalized, actionable career advice based on the user's profile.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            return {"success": True, "response": response.choices[0].message.content}

        except Exception as e:
            print(f"AI Service error: {str(e)}")
            return {
                "success": False,
                "response": "Sorry, I couldn't generate a response at this time.",
                "error": str(e),
            }

    def _build_career_prompt(
        self, user_profile: Dict[str, Any], question: Optional[str] = None
    ) -> str:
        """Build a detailed prompt for career advice based on user profile"""

        skills = user_profile.get("skills", [])
        experience = user_profile.get("experience", "")
        interests = user_profile.get("interests", [])
        current_role = user_profile.get("current_role", "")
        goals = user_profile.get("goals", [])

        prompt = f"""
        I'm a software engineer seeking career advice. Here's my profile:

        Current Role: {current_role}
        Experience Level: {experience}

        Technical Skills:
        {', '.join(skills) if skills else 'Not specified'}

        Career Interests:
        {', '.join(interests) if interests else 'Not specified'}

        Career Goals:
        {', '.join(goals) if goals else 'Not specified'}
        """

        if question:
            prompt += f"\n\nSpecific Question: {question}"
        else:
            prompt += "\n\nPlease provide personalized career advice including potential career paths, skills to develop, and actionable next steps."

        return prompt.strip()
