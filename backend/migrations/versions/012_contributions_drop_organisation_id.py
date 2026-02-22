"""Drop organisation_id from contributions

Revision ID: 012_contributions_drop_org_id
Revises: 011_sales_farm_id
Create Date: 2025-02-16

"""
from alembic import op
import sqlalchemy as sa

revision = "012_contributions_drop_org_id"
down_revision = "011_sales_farm_id"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text('ALTER TABLE "contributions" DROP COLUMN IF EXISTS organisation_id CASCADE'))


def downgrade():
    op.add_column("contributions", sa.Column("organisation_id", sa.String(36), nullable=True))
    op.create_index(op.f("ix_contributions_organisation_id"), "contributions", ["organisation_id"], unique=False)
    op.create_foreign_key(
        "contributions_organisation_id_fkey",
        "contributions",
        "organisations",
        ["organisation_id"],
        ["id"],
    )
