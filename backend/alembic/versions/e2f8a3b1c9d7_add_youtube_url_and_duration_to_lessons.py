"""add youtube_url and duration_minutes to lessons

Revision ID: e2f8a3b1c9d7
Revises: f845f9c2346c
Create Date: 2026-06-30 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e2f8a3b1c9d7'
down_revision: Union[str, Sequence[str], None] = 'd4b1c6a8f0e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('lessons', sa.Column('youtube_url', sa.String(length=500), nullable=True))
    op.add_column('lessons', sa.Column('duration_minutes', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('lessons', 'duration_minutes')
    op.drop_column('lessons', 'youtube_url')
