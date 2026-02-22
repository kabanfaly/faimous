"""Drop organisation_id from sales; add farm_id FK to farms

Revision ID: 011_sales_farm_id
Revises: 010_shareholder_email_required
Create Date: 2025-02-16

"""
from alembic import op
import sqlalchemy as sa

revision = "011_sales_farm_id"
down_revision = "010_shareholder_email_required"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text('ALTER TABLE "sales" DROP COLUMN IF EXISTS organisation_id CASCADE'))
    op.add_column("sales", sa.Column("farm_id", sa.String(36), nullable=True))
    op.create_foreign_key(
        "fk_sales_farm_id_farms",
        "sales",
        "farms",
        ["farm_id"],
        ["id"],
    )
    op.create_index(op.f("ix_sales_farm_id"), "sales", ["farm_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_sales_farm_id"), table_name="sales")
    op.drop_constraint("fk_sales_farm_id_farms", "sales", type_="foreignkey")
    op.drop_column("sales", "farm_id")
    op.add_column("sales", sa.Column("organisation_id", sa.String(36), nullable=True))
    op.create_index(op.f("ix_sales_organisation_id"), "sales", ["organisation_id"], unique=False)
    op.create_foreign_key(
        "sales_organisation_id_fkey",
        "sales",
        "organisations",
        ["organisation_id"],
        ["id"],
    )
