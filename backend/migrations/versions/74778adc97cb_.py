"""empty message

Revision ID: 74778adc97cb
Revises: 16dd08f5ab2b
Create Date: 2025-08-20 17:26:53.575590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '74778adc97cb'
down_revision: Union[str, None] = '16dd08f5ab2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    prompts_table = sa.Table(
        'prompts',
        sa.MetaData(),
        autoload_with=op.get_bind()
    )
    
    op.bulk_insert(prompts_table, [
        {
            'id': uuid.uuid4(),
            'title': 'Career Path Guidance',
            'prompt_text': 'What are the best career paths for someone with my skills and experience?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Skill Development',
            'prompt_text': 'What skills should I focus on developing next to advance my career?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Leadership Transition',
            'prompt_text': 'How can I transition from an individual contributor to a technical leadership role?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Industry Trends',
            'prompt_text': 'What are the current trends in software engineering that I should be aware of?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Salary Negotiation',
            'prompt_text': 'How can I effectively negotiate my salary and compensation package?'
        },
        {
            'id': uuid.uuid4(),
            'title': 'Work-Life Balance',
            'prompt_text': 'How can I maintain a healthy work-life balance while advancing my career?'
        }
    ])


def downgrade() -> None:
    op.execute("TRUNCATE TABLE prompts")
