"""Add new column

Revision ID: f0229c80def1
Revises: 8751885ef85c
Create Date: 2025-08-07 19:01:38.416439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0229c80def1'
down_revision: Union[str, Sequence[str], None] = '8751885ef85c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
