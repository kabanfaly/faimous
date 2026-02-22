"""Add farm_id FK to expenses

Revision ID: 006_expense_farm_id
Revises: 005_farm_location_to_city_id
Create Date: 2025-02-14

"""
import sqlalchemy as sa
from alembic import op


revision = "006_expense_farm_id"
down_revision = "005_farm_location_to_city_id"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("expenses", sa.Column("farm_id", sa.String(36), nullable=True))
    op.create_foreign_key(
        "fk_expenses_farm_id_farms",
        "expenses",
        "farms",
        ["farm_id"],
        ["id"],
    )
    op.create_index(op.f("ix_expenses_farm_id"), "expenses", ["farm_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_expenses_farm_id"), table_name="expenses")
    op.drop_constraint("fk_expenses_farm_id_farms", "expenses", type_="foreignkey")
    op.drop_column("expenses", "farm_id")
