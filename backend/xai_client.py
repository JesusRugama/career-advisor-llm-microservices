from openai import OpenAI
from config import settings

async def get_career_advice(user_profile, question=None):
    # Build the prompt first
    prompt = _build_career_prompt(user_profile, question)

    payload = {
        "model": "grok-4",
        'messages': [
            {
                'role': 'system',
                'content': 'You are a career advisor for software engineers. Provide personalized, actionable career advice based on the user\'s profile.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        "stream": False,
        'temperature': 0.7
    }

    print('prompt: ', prompt)

    # Get API key from settings
    print('api_key: ', settings.xai_api_key)
    
    # Set up OpenAI client with XAI configuration
    client = OpenAI(
        api_key=settings.xai_api_key,
        base_url=settings.xai_base_url,
    )

    return client.chat.completions.create(
        model=settings.xai_model,
        messages=[
            {"role": "system", "content": "You are a career advisor for software engineers. Provide personalized, actionable career advice based on the user's profile."},
            {"role": "user", "content": prompt}
        ]
    )

def _build_career_prompt(user_profile, question=None):
    """Build a detailed prompt for career advice based on user profile"""

    skills = user_profile.get('skills', [])
    experience = user_profile.get('experience', '')
    interests = user_profile.get('interests', [])
    current_role = user_profile.get('current_role', '')
    goals = user_profile.get('goals', [])

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