"""Make shareholders.email required (NOT NULL)

Revision ID: 010_shareholder_email_required
Revises: 009_wholesalers_products_etc
Create Date: 2025-02-16

"""
from alembic import op
import sqlalchemy as sa

revision = "010_shareholder_email_required"
down_revision = "009_wholesalers_products_etc"
branch_labels = None
depends_on = None


def upgrade():
    # Backfill any NULL emails with empty string, then alter to NOT NULL
    op.execute("UPDATE shareholders SET email = '' WHERE email IS NULL")
    op.alter_column(
        "shareholders",
        "email",
        existing_type=sa.String(255),
        nullable=False,
    )


def downgrade():
    op.alter_column(
        "shareholders",
        "email",
        existing_type=sa.String(255),
        nullable=True,
    )
