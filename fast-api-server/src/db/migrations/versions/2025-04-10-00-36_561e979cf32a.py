"""create fixture table
Revision ID: 561e979cf32a
Revises: 
Create Date: 2025-04-10 00:36:42.342830
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '561e979cf32a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "fixture",
        sa.Column(
            "id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False
        ),
        sa.Column("externalId", sa.String(length=200), nullable=False, unique=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("fixtureUrl", sa.String(length=200), nullable=False),
        sa.Column("demo", sa.Boolean(), nullable=True),
        sa.Column("statuses", postgresql.ARRAY(sa.VARCHAR()), nullable=True),
        sa.Column("createdDate", sa.String(length=200), nullable=True),
        sa.Column("modifiedDate", sa.String(length=200), nullable=True),
        sa.Column("createdBy", sa.String(length=200), nullable=True),
        sa.Column("createdAt", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updatedAt", postgresql.TIMESTAMP(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_table("fixture")
