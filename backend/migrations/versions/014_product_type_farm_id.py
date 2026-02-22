"""Add farm_id to product_types

Revision ID: 014_product_type_farm_id
Revises: 013_product_types
Create Date: 2025-02-16

"""
from alembic import op
import sqlalchemy as sa


revision = "014_product_type_farm_id"
down_revision = "013_product_types"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("product_types", sa.Column("farm_id", sa.String(36), nullable=True))
    op.create_index(op.f("ix_product_types_farm_id"), "product_types", ["farm_id"], unique=False)
    op.create_foreign_key(
        "fk_product_types_farm_id_farms",
        "product_types",
        "farms",
        ["farm_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("fk_product_types_farm_id_farms", "product_types", type_="foreignkey")
    op.drop_index(op.f("ix_product_types_farm_id"), table_name="product_types")
    op.drop_column("product_types", "farm_id")

