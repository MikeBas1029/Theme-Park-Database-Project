"""Merged branch heads

Revision ID: 959d713bd309
Revises: 3e630a568ad6, a2e9e16127a2
Create Date: 2024-10-26 18:05:45.692338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '959d713bd309'
down_revision: Union[str, None] = ('3e630a568ad6', 'a2e9e16127a2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
