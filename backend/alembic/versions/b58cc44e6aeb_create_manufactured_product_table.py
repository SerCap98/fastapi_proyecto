"""create MANUFACTURED_PRODUCT table

Revision ID: b58cc44e6aeb
Revises: 5dc5b2323897
Create Date: 2024-01-11 15:04:18.252984

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'b58cc44e6aeb'
down_revision = '5dc5b2323897'
branch_labels = None
depends_on = None

def create_manufactured_product_table():
    op.create_table(
        "manufactured_product",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("id_product", UUID, sa.ForeignKey("product.id"), nullable=False),
        sa.Column("lot_number", sa.Text, nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),        
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_manufactured_product_table()


def downgrade() -> None:
    op.drop_table("manufactured_product")

