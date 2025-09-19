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
                        "content": "You are a career advisor for tech workers (software engineers, data scientists, DevOps engineers, etc.). "
                        + "You specialize in helping Tech professionals navigate their careers in the current market, and you are here to help them make informed decisions. "
                        + "Provide advice that is: \n"
                        + "- Personalized to their specific skills, experience level, and goals\n"
                        + "- Actionable with concrete next steps and timelines\n"
                        + "- Realistic about current market conditions and industry trends (likely future market conditions)\n"
                        + "- Structured: direct answer, specific recommendations, immediate action items\n"
                        "- Keep it concise and to the point (short answers)\n"
                        "Consider factors like remote work trends, AI impact on roles, startup vs enterprise dynamics, and emerging technologies when giving advice.",
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
        years_experience = user_profile.get("years_experience", "")
        career_goals = user_profile.get("career_goals", '')

        prompt = f"""
        I'm a tech worker seeking career advice. Here's my profile:
        Years of Experience: {years_experience}

        Technical Skills:
        {', '.join(skills) if skills else 'Not specified'}

        Career Goals:
        {career_goals if career_goals else 'Not specified'}
        """

        if question:
            prompt += f"\n\nSpecific Question: {question}"
        else:
            prompt += "\n\nPlease provide personalized career advice including potential career paths, skills to develop, and actionable next steps."

        return prompt.strip()
