"""Make products.product_type_id NOT NULL

Revision ID: 016_product_type_not_null
Revises: 015_drop_products_farm_id
Create Date: 2025-02-16

"""
from alembic import op
import sqlalchemy as sa

revision = "016_product_type_not_null"
down_revision = "015_drop_products_farm_id"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    # Ensure there is a default ProductType to use for existing NULLs
    default_id = conn.execute(sa.text(
        """
        INSERT INTO product_types (id, name)
        VALUES (gen_random_uuid()::text, 'Unknown')
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
        """
    )).scalar()

    conn.execute(
        sa.text(
            "UPDATE products SET product_type_id = :pid WHERE product_type_id IS NULL"
        ),
        {"pid": default_id},
    )

    op.alter_column("products", "product_type_id", existing_type=sa.String(36), nullable=False)


def downgrade():
    op.alter_column("products", "product_type_id", existing_type=sa.String(36), nullable=True)
