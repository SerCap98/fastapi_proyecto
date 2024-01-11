"""create PRODUCTION_MATERIAL_USAGE table

Revision ID: 84bd788205e0
Revises: b58cc44e6aeb
Create Date: 2024-01-11 15:04:41.105151

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '84bd788205e0'
down_revision = 'b58cc44e6aeb'
branch_labels = None
depends_on = None


def create_production_material_usage_table():
    op.create_table(
        "production_material_usage",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("id_manufactured_product", UUID, sa.ForeignKey("manufactured_product.id"), nullable=False),
        sa.Column("id_factory_inventory", UUID, sa.ForeignKey("factory_raw_material_inventory.id"), nullable=False),
        sa.Column("quantity", sa.Float, nullable=False),        
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_production_material_usage_table()

def downgrade() -> None:
    op.drop_table("production_material_usage")

