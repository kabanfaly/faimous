"""Drop farm_id from products

Revision ID: 015_drop_products_farm_id
Revises: 014_product_type_farm_id
Create Date: 2025-02-16

"""
from alembic import op
import sqlalchemy as sa

revision = "015_drop_products_farm_id"
down_revision = "014_product_type_farm_id"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index(op.f("ix_products_farm_id"), table_name="products")
    op.drop_constraint("fk_products_farm_id_farms", "products", type_="foreignkey")
    op.drop_column("products", "farm_id")


def downgrade():
    op.add_column("products", sa.Column("farm_id", sa.String(36), nullable=True))
    op.create_foreign_key(
        "fk_products_farm_id_farms",
        "products",
        "farms",
        ["farm_id"],
        ["id"],
    )
    op.create_index(op.f("ix_products_farm_id"), "products", ["farm_id"], unique=False)
