"""Drop organisation FK from egg_productions, flock_records, daily_operations, farms, expenses, suppliers

Revision ID: 007_drop_org_fk
Revises: 006_expense_farm_id
Create Date: 2025-02-14

"""
from alembic import op

revision = "007_drop_org_fk"
down_revision = "006_expense_farm_id"
branch_labels = None
depends_on = None

# PostgreSQL default FK names when not explicitly set: {tablename}_{columnname}_fkey
TABLES = [
    "egg_productions",
    "flock_records",
    "daily_operations",
    "farms",
    "expenses",
    "suppliers",
]


def upgrade():
    for table in TABLES:
        constraint_name = f"{table}_organisation_id_fkey"
        op.drop_constraint(constraint_name, table, type_="foreignkey")


def downgrade():
    for table in TABLES:
        constraint_name = f"{table}_organisation_id_fkey"
        op.create_foreign_key(
            constraint_name,
            table,
            "organisations",
            ["organisation_id"],
            ["id"],
        )
