"""Drop organisation_id column from egg_productions, flock_records, daily_operations, expenses, suppliers

Revision ID: 008_drop_org_id
Revises: 007_drop_org_fk
Create Date: 2025-02-14

"""
from alembic import op
import sqlalchemy as sa

revision = "008_drop_org_id"
down_revision = "007_drop_org_fk"
branch_labels = None
depends_on = None

TABLES = [
    "egg_productions",
    "flock_records",
    "daily_operations",
    "expenses",
    "suppliers",
]


def upgrade():
    for table in TABLES:
        op.drop_index(op.f(f"ix_{table}_organisation_id"), table_name=table)
        op.drop_column(table, "organisation_id")


def downgrade():
    for table in TABLES:
        op.add_column(table, sa.Column("organisation_id", sa.String(36), nullable=True))
        op.create_index(op.f(f"ix_{table}_organisation_id"), table, ["organisation_id"], unique=False)
        # Note: downgrade does not repopulate organisation_id; backfill would be required for data integrity.
