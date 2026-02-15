"""Set default user.role to 'user'

Revision ID: 004_user_role_default
Revises: 003_user_status_to_activated
Create Date: 2025-02-12

"""
from alembic import op


revision = "004_user_role_default"
down_revision = "003_user_status_to_activated"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'user'")


def downgrade():
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
