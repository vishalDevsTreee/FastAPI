"""add last few columns to posts table

Revision ID: 616f7d406b41
Revises: 043b2249011c
Create Date: 2026-10-05 23:30:17.101634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '616f7d406b41'
down_revision: Union[str, Sequence[str], None] = '043b2249011c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
