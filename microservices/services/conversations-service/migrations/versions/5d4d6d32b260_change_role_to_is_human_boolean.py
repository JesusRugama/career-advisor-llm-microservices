"""change role to is_human boolean

Revision ID: 5d4d6d32b260
Revises: 992f135ae62b
Create Date: 2025-09-10 20:44:14.378465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d4d6d32b260'
down_revision: Union[str, None] = '992f135ae62b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new is_human column
    op.add_column('messages', sa.Column('is_human', sa.Boolean(), nullable=True))
    
    # Update existing data: 'user' -> True, 'assistant' -> False
    op.execute("UPDATE messages SET is_human = CASE WHEN role = 'user' THEN true ELSE false END")
    
    # Make is_human not nullable
    op.alter_column('messages', 'is_human', nullable=False)
    
    # Drop the old role column
    op.drop_column('messages', 'role')


def downgrade() -> None:
    # Add back role column
    op.add_column('messages', sa.Column('role', sa.String(length=50), nullable=True))
    
    # Update data: True -> 'user', False -> 'assistant'
    op.execute("UPDATE messages SET role = CASE WHEN is_human = true THEN 'user' ELSE 'assistant' END")
    
    # Make role not nullable
    op.alter_column('messages', 'role', nullable=False)
    
    # Drop is_human column
    op.drop_column('messages', 'is_human')
