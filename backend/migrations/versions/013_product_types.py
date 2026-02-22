"""Create product_types table; add product_type_id to products; drop products.type

Revision ID: 013_product_types
Revises: 012_contributions_drop_org_id
Create Date: 2025-02-16

"""
from alembic import op
import sqlalchemy as sa

revision = "013_product_types"
down_revision = "012_contributions_drop_org_id"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "product_types",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
    )
    op.create_index(op.f("ix_product_types_name"), "product_types", ["name"], unique=True)

    # Seed product_types from distinct non-null products.type (PostgreSQL)
    conn = op.get_bind()
    conn.execute(
        sa.text("""
            INSERT INTO product_types (id, name)
            SELECT gen_random_uuid()::text, t.type
            FROM (SELECT DISTINCT type FROM products WHERE type IS NOT NULL AND type != '') AS t(type)
        """)
    )

    op.add_column("products", sa.Column("product_type_id", sa.String(36), nullable=True))
    op.create_foreign_key(
        "fk_products_product_type_id_product_types",
        "products",
        "product_types",
        ["product_type_id"],
        ["id"],
    )
    op.create_index(op.f("ix_products_product_type_id"), "products", ["product_type_id"], unique=False)

    # Backfill: set product_type_id from matching product_types.name = products.type
    conn.execute(
        sa.text("""
            UPDATE products p
            SET product_type_id = pt.id
            FROM product_types pt
            WHERE p.type IS NOT NULL AND p.type != '' AND pt.name = p.type
        """)
    )

    op.drop_column("products", "type")


def downgrade():
    op.add_column("products", sa.Column("type", sa.String(50), nullable=True))

    conn = op.get_bind()
    conn.execute(
        sa.text("""
            UPDATE products p
            SET type = pt.name
            FROM product_types pt
            WHERE p.product_type_id = pt.id
        """)
    )

    op.drop_index(op.f("ix_products_product_type_id"), table_name="products")
    op.drop_constraint("fk_products_product_type_id_product_types", "products", type_="foreignkey")
    op.drop_column("products", "product_type_id")

    op.drop_index(op.f("ix_product_types_name"), table_name="product_types")
    op.drop_table("product_types")
