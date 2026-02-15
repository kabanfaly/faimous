"""Initial schema

Revision ID: 001_initial
Revises:
Create Date: 2025-02-10

"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial"
down_revision = None


def upgrade():
    op.create_table(
        "organisations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("currency_default", sa.String(10), nullable=True),
        sa.Column("language_default", sa.String(10), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "currencies",
        sa.Column("code", sa.String(10), nullable=False),
        sa.Column("symbol", sa.String(10), nullable=True),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_table(
        "farms",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("location", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_farms_organisation_id"), "farms", ["organisation_id"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("gender", sa.String(20), nullable=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("language", sa.String(10), nullable=True),
        sa.Column("status", sa.String(20), nullable=True),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_organisation_id"), "users", ["organisation_id"], unique=False)
    op.create_table(
        "cities",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("prefecture", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cities_organisation_id"), "cities", ["organisation_id"], unique=False)
    op.create_table(
        "exchange_rates",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("from_currency", sa.String(10), nullable=False),
        sa.Column("to_currency", sa.String(10), nullable=False),
        sa.Column("rate", sa.Numeric(18, 6), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["from_currency"], ["currencies.code"]),
        sa.ForeignKeyConstraint(["to_currency"], ["currencies.code"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_exchange_rates_date"), "exchange_rates", ["date"], unique=False)
    op.create_index(op.f("ix_exchange_rates_from_currency"), "exchange_rates", ["from_currency"], unique=False)
    op.create_index(op.f("ix_exchange_rates_to_currency"), "exchange_rates", ["to_currency"], unique=False)
    op.create_table(
        "wholesalers",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("city_id", sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_wholesalers_organisation_id"), "wholesalers", ["organisation_id"], unique=False)
    op.create_table(
        "suppliers",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("city_id", sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_suppliers_organisation_id"), "suppliers", ["organisation_id"], unique=False)
    op.create_table(
        "products",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(50), nullable=True),
        sa.Column("unit", sa.String(50), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_organisation_id"), "products", ["organisation_id"], unique=False)
    op.create_table(
        "expense_categories",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_expense_categories_organisation_id"), "expense_categories", ["organisation_id"], unique=False)
    op.create_table(
        "shareholders",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_shareholders_organisation_id"), "shareholders", ["organisation_id"], unique=False)
    op.create_table(
        "egg_productions",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("farm_id", sa.String(36), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("eggs_count", sa.Integer(), nullable=True),
        sa.Column("broken_count", sa.Integer(), nullable=True),
        sa.Column("trays", sa.Integer(), nullable=True),
        sa.Column("remaining", sa.Integer(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_egg_productions_organisation_id"), "egg_productions", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_egg_productions_date"), "egg_productions", ["date"], unique=False)
    op.create_table(
        "flock_records",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("farm_id", sa.String(36), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("total_hens", sa.Integer(), nullable=True),
        sa.Column("dead", sa.Integer(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_flock_records_organisation_id"), "flock_records", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_flock_records_date"), "flock_records", ["date"], unique=False)
    op.create_table(
        "daily_operations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("farm_id", sa.String(36), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("period", sa.String(50), nullable=True),
        sa.Column("collect1", sa.Integer(), nullable=True),
        sa.Column("collect2", sa.Integer(), nullable=True),
        sa.Column("collect3", sa.Integer(), nullable=True),
        sa.Column("collect4", sa.Integer(), nullable=True),
        sa.Column("broken", sa.Integer(), nullable=True),
        sa.Column("hens", sa.Integer(), nullable=True),
        sa.Column("dead", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_daily_operations_organisation_id"), "daily_operations", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_daily_operations_date"), "daily_operations", ["date"], unique=False)
    op.create_table(
        "sales",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("type", sa.String(50), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("unit_price", sa.Numeric(18, 2), nullable=True),
        sa.Column("total_price", sa.Numeric(18, 2), nullable=True),
        sa.Column("theoretical_price", sa.Numeric(18, 2), nullable=True),
        sa.Column("price_diff", sa.Numeric(18, 2), nullable=True),
        sa.Column("wholesaler_id", sa.String(36), nullable=True),
        sa.Column("payment_status", sa.String(50), nullable=True),
        sa.Column("currency", sa.String(10), nullable=True),
        sa.Column("amount_base", sa.Numeric(18, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.ForeignKeyConstraint(["wholesaler_id"], ["wholesalers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sales_organisation_id"), "sales", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_sales_date"), "sales", ["date"], unique=False)
    op.create_table(
        "purchases",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("supplier_id", sa.String(36), nullable=True),
        sa.Column("product_id", sa.String(36), nullable=True),
        sa.Column("unit_price", sa.Numeric(18, 2), nullable=True),
        sa.Column("quantity", sa.Numeric(18, 2), nullable=True),
        sa.Column("total_price", sa.Numeric(18, 2), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("currency", sa.String(10), nullable=True),
        sa.Column("amount_base", sa.Numeric(18, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_purchases_organisation_id"), "purchases", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_purchases_date"), "purchases", ["date"], unique=False)
    op.create_table(
        "payments_received",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("sale_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("payment_method", sa.String(50), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["sale_id"], ["sales.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_payments_received_sale_id"), "payments_received", ["sale_id"], unique=False)
    op.create_table(
        "supplier_payments",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("purchase_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("payment_method", sa.String(50), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["purchase_id"], ["purchases.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_supplier_payments_purchase_id"), "supplier_payments", ["purchase_id"], unique=False)
    op.create_table(
        "stock_movements",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("product_id", sa.String(36), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("quantity", sa.Numeric(18, 2), nullable=False),
        sa.Column("price", sa.Numeric(18, 2), nullable=True),
        sa.Column("movement_type", sa.String(50), nullable=True),
        sa.Column("purchase_id", sa.String(36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["purchase_id"], ["purchases.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_stock_movements_organisation_id"), "stock_movements", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_stock_movements_date"), "stock_movements", ["date"], unique=False)
    op.create_table(
        "expenses",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category_id", sa.String(36), nullable=True),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("currency", sa.String(10), nullable=True),
        sa.Column("amount_base", sa.Numeric(18, 2), nullable=True),
        sa.Column("invoice_file", sa.String(500), nullable=True),
        sa.Column("payment_method", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["expense_categories.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_expenses_organisation_id"), "expenses", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_expenses_date"), "expenses", ["date"], unique=False)
    op.create_table(
        "feed_preparations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("quantity_kg", sa.Numeric(18, 2), nullable=False),
        sa.Column("ratio", sa.String(100), nullable=True),
        sa.Column("hens_available", sa.Integer(), nullable=True),
        sa.Column("expected_end_date", sa.Date(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_feed_preparations_organisation_id"), "feed_preparations", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_feed_preparations_date"), "feed_preparations", ["date"], unique=False)
    op.create_table(
        "contributions",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("organisation_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("shareholder_id", sa.String(36), nullable=True),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("currency", sa.String(10), nullable=True),
        sa.Column("amount_base", sa.Numeric(18, 2), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.ForeignKeyConstraint(["shareholder_id"], ["shareholders.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contributions_organisation_id"), "contributions", ["organisation_id"], unique=False)
    op.create_index(op.f("ix_contributions_date"), "contributions", ["date"], unique=False)


def downgrade():
    op.drop_table("contributions")
    op.drop_table("feed_preparations")
    op.drop_table("expenses")
    op.drop_table("stock_movements")
    op.drop_table("supplier_payments")
    op.drop_table("payments_received")
    op.drop_table("purchases")
    op.drop_table("sales")
    op.drop_table("daily_operations")
    op.drop_table("flock_records")
    op.drop_table("egg_productions")
    op.drop_table("shareholders")
    op.drop_table("expense_categories")
    op.drop_table("products")
    op.drop_table("suppliers")
    op.drop_table("wholesalers")
    op.drop_table("exchange_rates")
    op.drop_table("cities")
    op.drop_table("users")
    op.drop_table("farms")
    op.drop_table("currencies")
    op.drop_table("organisations")
