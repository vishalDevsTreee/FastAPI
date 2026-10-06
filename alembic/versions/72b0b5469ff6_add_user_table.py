"""add user table

Revision ID: 72b0b5469ff6
Revises: b7669fd647e2
Create Date: 2026-10-05 17:00:13.260488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72b0b5469ff6'
down_revision: Union[str, Sequence[str], None] = 'b7669fd647e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), 
                              nullable=False))
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
