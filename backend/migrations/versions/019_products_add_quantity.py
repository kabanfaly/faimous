"""Add quantity to products

Revision ID: 019_products_add_quantity
Revises: 018_drop_farms_org_id
Create Date: 2026-02-18

"""
from alembic import op
import sqlalchemy as sa

revision = "019_products_add_quantity"
down_revision = "018_drop_farms_org_id"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("products", sa.Column("quantity", sa.Numeric(18, 2), nullable=True))


def downgrade():
    op.drop_column("products", "quantity")
