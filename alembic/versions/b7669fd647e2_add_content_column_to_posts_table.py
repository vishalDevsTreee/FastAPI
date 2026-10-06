"""add content column to posts table

Revision ID: b7669fd647e2
Revises: f5a666e79d13
Create Date: 2026-10-05 16:49:16.123315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7669fd647e2'
down_revision: Union[str, Sequence[str], None] = 'f5a666e79d13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
