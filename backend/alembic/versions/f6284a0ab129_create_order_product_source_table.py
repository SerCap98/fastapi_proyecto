"""create ORDER_PRODUCT_SOURCE table

Revision ID: f6284a0ab129
Revises: 6196e3b31033
Create Date: 2024-01-11 15:06:03.058506

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'f6284a0ab129'
down_revision = '6196e3b31033'
branch_labels = None
depends_on = None


def create_order_product_source_table():
    op.create_table(
        "order_product_source",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("id_warehouse_product", UUID, sa.ForeignKey("warehouse_product_inventory.id"), nullable=False),
        sa.Column("id_order", UUID, sa.ForeignKey("order_product.id"), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),       
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_order_product_source_table()

def downgrade() -> None:
    op.drop_table("order_product_source")