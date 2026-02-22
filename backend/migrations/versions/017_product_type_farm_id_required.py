"""Make product_types.farm_id NOT NULL

Revision ID: 017_product_type_farm_id_required
Revises: 016_product_type_not_null
Create Date: 2025-02-18

"""
from alembic import op
import sqlalchemy as sa

revision = "017_pt_farm_req"
down_revision = "016_product_type_not_null"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            UPDATE product_types
            SET farm_id = (SELECT id FROM farms LIMIT 1)
            WHERE farm_id IS NULL
            """
        )
    )
    op.alter_column(
        "product_types",
        "farm_id",
        existing_type=sa.String(36),
        nullable=False,
    )


def downgrade():
    op.alter_column(
        "product_types",
        "farm_id",
        existing_type=sa.String(36),
        nullable=True,
    )
