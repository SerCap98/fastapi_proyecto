"""create WAREHOUSE_PRODUCT_INVENTORY table

Revision ID: be75eaae9eb5
Revises: 84bd788205e0
Create Date: 2024-01-11 15:05:07.707530

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'be75eaae9eb5'
down_revision = '84bd788205e0'
branch_labels = None
depends_on = None

def create_warehouse_product_inventory_table():
    op.create_table(
        "warehouse_product_inventory",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("id_warehouse", UUID, sa.ForeignKey("warehouse.id"), nullable=False),
        sa.Column("id_manufactured_product", UUID, sa.ForeignKey("manufactured_product.id"), nullable=False),
        sa.Column("available_product", sa.Integer, nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )


def upgrade() -> None:
    create_warehouse_product_inventory_table()


def downgrade() -> None:
    op.drop_table("warehouse_product_inventory")