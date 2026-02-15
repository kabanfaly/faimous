"""Rename user status to activated (boolean)

Revision ID: 003_user_status_to_activated
Revises: 002_user_gender_enum
Create Date: 2025-02-12

"""
from alembic import op
import sqlalchemy as sa


revision = "003_user_status_to_activated"
down_revision = "002_user_gender_enum"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("activated", sa.Boolean(), nullable=True, server_default=sa.true()),
    )
    op.execute(
        "UPDATE users SET activated = COALESCE(status = 'active', true)"
    )
    op.alter_column(
        "users",
        "activated",
        nullable=False,
        server_default=sa.true(),
    )
    op.drop_column("users", "status")


def downgrade():
    op.add_column(
        "users",
        sa.Column("status", sa.String(20), nullable=True),
    )
    op.execute(
        "UPDATE users SET status = CASE WHEN activated THEN 'active' ELSE 'inactive' END"
    )
    op.drop_column("users", "activated")
