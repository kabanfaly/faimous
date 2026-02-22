"""Rename farm location to city_id with FK to cities

Revision ID: 005_farm_location_to_city_id
Revises: 004_user_role_default
Create Date: 2025-02-14

"""
import sqlalchemy as sa
from alembic import op


revision = "005_farm_location_to_city_id"
down_revision = "004_user_role_default"
branch_labels = None
depends_on = None


def upgrade():
    # Clear existing location values so we can add FK (old values are not city IDs)
    op.execute("UPDATE farms SET location = NULL WHERE location IS NOT NULL")
    with op.batch_alter_table("farms", schema=None) as batch_op:
        batch_op.alter_column(
            "location",
            new_column_name="city_id",
            existing_type=sa.String(255),
            existing_nullable=True,
        )
        batch_op.create_foreign_key(
            "fk_farms_city_id_cities",
            "cities",
            ["city_id"],
            ["id"],
        )
        batch_op.create_index(op.f("ix_farms_city_id"), ["city_id"], unique=False)


def downgrade():
    with op.batch_alter_table("farms", schema=None) as batch_op:
        batch_op.drop_index(op.f("ix_farms_city_id"), table_name="farms")
        batch_op.drop_constraint("fk_farms_city_id_cities", type_="foreignkey")
        batch_op.alter_column(
            "city_id",
            new_column_name="location",
            existing_type=sa.String(255),
            existing_nullable=True,
        )
