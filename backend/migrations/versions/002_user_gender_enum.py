"""User gender as enum

Revision ID: 002_user_gender_enum
Revises: 001_initial
Create Date: 2025-02-10

"""
from alembic import op
import sqlalchemy as sa


revision = "002_user_gender_enum"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TYPE gender_enum AS ENUM ('male', 'female')")
    op.execute(
        "UPDATE users SET gender = 'male' WHERE gender IS NULL OR gender NOT IN ('male', 'female')"
    )
    op.execute(
        "ALTER TABLE users ALTER COLUMN gender TYPE gender_enum USING gender::gender_enum"
    )
    op.execute("ALTER TABLE users ALTER COLUMN gender SET DEFAULT 'male'")
    op.execute("ALTER TABLE users ALTER COLUMN gender SET NOT NULL")


def downgrade():
    op.execute("ALTER TABLE users ALTER COLUMN gender DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN gender TYPE VARCHAR(20) USING gender::text")
    op.execute("ALTER TABLE users ALTER COLUMN gender DROP NOT NULL")
    op.execute("DROP TYPE gender_enum")
