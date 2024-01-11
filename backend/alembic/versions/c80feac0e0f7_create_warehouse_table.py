"""create WAREHOUSE table

Revision ID: c80feac0e0f7
Revises: aff5b76378a3
Create Date: 2024-01-11 15:01:48.039023

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

type1 = sa.Enum('MAIN', 'CONSIGNED', name='type1')

# revision identifiers, used by Alembic.
revision = 'c80feac0e0f7'
down_revision = 'aff5b76378a3'
branch_labels = None
depends_on = None


def create_warehouse_table():
    op.create_table(
        "warehouse",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("type", type1, nullable=False),
        sa.Column("type_num", sa.Integer, nullable=False),        
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_warehouse_table()

def downgrade() -> None:
    op.drop_table("warehouse")