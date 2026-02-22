"""Drop organisation_id from wholesalers, products, purchases, stock_movements; add farm_id to products

Revision ID: 009_wholesalers_products_etc
Revises: 008_drop_org_id
Create Date: 2025-02-14

"""
from alembic import op
import sqlalchemy as sa

revision = "009_wholesalers_products_etc"
down_revision = "008_drop_org_id"
branch_labels = None
depends_on = None

TABLES_DROP_ORG = [
    "wholesalers",
    "products",
    "purchases",
    "stock_movements",
]


def upgrade():
    conn = op.get_bind()
    for table in TABLES_DROP_ORG:
        # CASCADE drops the column and any dependent FK constraint and index
        conn.execute(sa.text(f'ALTER TABLE "{table}" DROP COLUMN IF EXISTS organisation_id CASCADE'))

    op.add_column("products", sa.Column("farm_id", sa.String(36), nullable=True))
    op.create_foreign_key(
        "fk_products_farm_id_farms",
        "products",
        "farms",
        ["farm_id"],
        ["id"],
    )
    op.create_index(op.f("ix_products_farm_id"), "products", ["farm_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_products_farm_id"), table_name="products")
    op.drop_constraint("fk_products_farm_id_farms", "products", type_="foreignkey")
    op.drop_column("products", "farm_id")

    for table in TABLES_DROP_ORG:
        op.add_column(table, sa.Column("organisation_id", sa.String(36), nullable=True))
        op.create_index(op.f(f"ix_{table}_organisation_id"), table, ["organisation_id"], unique=False)
        op.create_foreign_key(
            f"{table}_organisation_id_fkey",
            table,
            "organisations",
            ["organisation_id"],
            ["id"],
        )
