"""create RAW_MATERIAL table

Revision ID: 450c129f2b3f
Revises: 492eec39b72d
Create Date: 2024-01-11 14:59:33.834697

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '450c129f2b3f'
down_revision = '492eec39b72d'
branch_labels = None
depends_on = None

def create_raw_material_table():
    op.create_table(
        "raw_material",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("code", sa.Text, nullable=False,unique=True),
        sa.Column("created_by", UUID, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by", UUID, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )

def upgrade() -> None:
    create_raw_material_table()


def downgrade() -> None:
    op.drop_table("raw_material")
