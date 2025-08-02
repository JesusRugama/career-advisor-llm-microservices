from fastapi import APIRouter
from xai_client import get_career_advice

router = APIRouter()

@router.post("/")
async def post_career_advice_question():
    result = await get_career_advice(HARDCODED_USER_PROFILE)
    return result


# Hardcoded user data (will be replaced with database later)
HARDCODED_USER_PROFILE = {
    'name': 'Jesus',
    'current_role': 'Software Engineer',
    'experience': '5+ years',
    'skills': [
        'Python', 'Django', 'JavaScript', 'React', 'Next.js',
        'PostgreSQL', 'AWS', 'Docker', 'Git', 'REST APIs'
    ],
    'interests': [
        'Full-stack development', 'AI/ML', 'Cloud architecture',
        'Product development', 'Team leadership'
    ],
    'goals': [
        'Become a technical lead', 'Learn more about AI/ML',
        'Build scalable products', 'Mentor other developers'
    ]
}
