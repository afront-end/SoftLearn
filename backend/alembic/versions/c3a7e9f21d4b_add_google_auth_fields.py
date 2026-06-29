"""add google auth fields to users

Revision ID: c3a7e9f21d4b
Revises: f845f9c2346c
Create Date: 2026-06-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c3a7e9f21d4b'
down_revision: Union[str, Sequence[str], None] = 'b8b9bf6a4700'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'password_hash', existing_type=sa.String(255), nullable=True)
    op.add_column('users', sa.Column('google_id', sa.String(255), nullable=True))
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_google_id'), table_name='users')
    op.drop_column('users', 'google_id')
    op.alter_column('users', 'password_hash', existing_type=sa.String(255), nullable=False)
