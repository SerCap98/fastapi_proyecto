"""create FACTORY_RAW_MATERIAL_INVENTORY table

Revision ID: 5fd0bda9a45c
Revises: c80feac0e0f7
Create Date: 2024-01-11 15:02:24.630330

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '5fd0bda9a45c'
down_revision = 'c80feac0e0f7'
branch_labels = None
depends_on = None



def create_factory_raw_material_inventory_table():
    op.create_table(
        "factory_raw_material_inventory",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("id_factory", UUID(as_uuid=True), sa.ForeignKey("factory.id"), nullable=False),
        sa.Column("id_raw_material", UUID(as_uuid=True), sa.ForeignKey("raw_material.id"), nullable=False),
        sa.Column("min_quantity", sa.Float, nullable=False),
        sa.Column("quantity", sa.Float, nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_factory_raw_material_inventory_table()


def downgrade() -> None:
    op.drop_table("factory_raw_material_inventory")
