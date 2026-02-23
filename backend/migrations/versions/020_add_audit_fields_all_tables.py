"""Add audit fields to all tables

Revision ID: 020_audit_fields_all
Revises: 019_products_add_quantity
Create Date: 2026-02-18

"""
from alembic import op
import sqlalchemy as sa

revision = "020_audit_fields_all"
down_revision = "019_products_add_quantity"
branch_labels = None
depends_on = None


def upgrade():
    # Tables without created_at before this migration
    for table in [
        "products",
        "farms",
        "product_types",
        "wholesalers",
        "suppliers",
        "expense_categories",
        "currencies",
        "exchange_rates",
        "cities",
        "shareholders",
    ]:
        op.add_column(table, sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False))

    # Add updated_at to all tables except users (already has updated_at)
    for table in [
        "products",
        "organisations",
        "farms",
        "product_types",
        "contributions",
        "sales",
        "payments_received",
        "stock_movements",
        "purchases",
        "supplier_payments",
        "wholesalers",
        "suppliers",
        "expenses",
        "daily_operations",
        "flock_records",
        "egg_productions",
        "feed_preparations",
        "expense_categories",
        "currencies",
        "exchange_rates",
        "cities",
        "shareholders",
    ]:
        op.add_column(table, sa.Column("updated_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False))

    # Add created_by/updated_by to all tables
    for table in [
        "products",
        "organisations",
        "farms",
        "product_types",
        "contributions",
        "sales",
        "payments_received",
        "stock_movements",
        "purchases",
        "supplier_payments",
        "wholesalers",
        "suppliers",
        "expenses",
        "daily_operations",
        "flock_records",
        "egg_productions",
        "users",
        "feed_preparations",
        "expense_categories",
        "currencies",
        "exchange_rates",
        "cities",
        "shareholders",
    ]:
        op.add_column(table, sa.Column("created_by", sa.String(255), nullable=True))
        op.add_column(table, sa.Column("updated_by", sa.String(255), nullable=True))


def downgrade():
    for table in [
        "products",
        "organisations",
        "farms",
        "product_types",
        "contributions",
        "sales",
        "payments_received",
        "stock_movements",
        "purchases",
        "supplier_payments",
        "wholesalers",
        "suppliers",
        "expenses",
        "daily_operations",
        "flock_records",
        "egg_productions",
        "users",
        "feed_preparations",
        "expense_categories",
        "currencies",
        "exchange_rates",
        "cities",
        "shareholders",
    ]:
        op.drop_column(table, "updated_by")
        op.drop_column(table, "created_by")

    for table in [
        "products",
        "organisations",
        "farms",
        "product_types",
        "contributions",
        "sales",
        "payments_received",
        "stock_movements",
        "purchases",
        "supplier_payments",
        "wholesalers",
        "suppliers",
        "expenses",
        "daily_operations",
        "flock_records",
        "egg_productions",
        "feed_preparations",
        "expense_categories",
        "currencies",
        "exchange_rates",
        "cities",
        "shareholders",
    ]:
        op.drop_column(table, "updated_at")

    for table in [
        "products",
        "farms",
        "product_types",
        "wholesalers",
        "suppliers",
        "expense_categories",
        "currencies",
        "exchange_rates",
        "cities",
        "shareholders",
    ]:
        op.drop_column(table, "created_at")
