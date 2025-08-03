from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_predefined_prompts():
    """
    Get predefined career advice prompts to help users get started
    """
    prompts = [
        {
            'id': 1,
            'title': 'Career Path Guidance',
            'prompt': 'What are the best career paths for someone with my skills and experience?'
        },
        {
            'id': 2,
            'title': 'Skill Development',
            'prompt': 'What skills should I focus on developing next to advance my career?'
        },
        {
            'id': 3,
            'title': 'Leadership Transition',
            'prompt': 'How can I transition from an individual contributor to a technical leadership role?'
        },
        {
            'id': 4,
            'title': 'Industry Trends',
            'prompt': 'What are the current trends in software engineering that I should be aware of?'
        },
        {
            'id': 5,
            'title': 'Salary Negotiation',
            'prompt': 'How can I effectively negotiate my salary and compensation package?'
        },
        {
            'id': 6,
            'title': 'Work-Life Balance',
            'prompt': 'How can I maintain a healthy work-life balance while advancing my career?'
        }
    ]

    return {
        'success': True,
        'prompts': prompts
    }