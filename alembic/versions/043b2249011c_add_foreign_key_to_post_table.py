"""add foreign-key to post table

Revision ID: 043b2249011c
Revises: 72b0b5469ff6
Create Date: 2026-10-05 18:12:30.175813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '043b2249011c'
down_revision: Union[str, Sequence[str], None] = '72b0b5469ff6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('ower_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['ower_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
