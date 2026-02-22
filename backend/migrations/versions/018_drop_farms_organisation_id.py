"""Drop organisation_id from farms

Revision ID: 018_drop_farms_org_id
Revises: 017_pt_farm_req
Create Date: 2026-02-18

"""
from alembic import op
import sqlalchemy as sa

revision = "018_drop_farms_org_id"
down_revision = "017_pt_farm_req"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index(op.f("ix_farms_organisation_id"), table_name="farms")
    op.drop_column("farms", "organisation_id")


def downgrade():
    op.add_column("farms", sa.Column("organisation_id", sa.String(36), nullable=False))
    op.create_index(op.f("ix_farms_organisation_id"), "farms", ["organisation_id"], unique=False)
