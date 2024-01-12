"""create ORDER_PRODUCT table

Revision ID: 015f4d6c69e6
Revises: be75eaae9eb5
Create Date: 2024-01-11 15:05:29.796310

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID



# revision identifiers, used by Alembic.
revision = '015f4d6c69e6'
down_revision = 'be75eaae9eb5'
branch_labels = None
depends_on = None

def create_order_product_table():
    op.create_table(
        "order_product",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("id_product", UUID, sa.ForeignKey("product.id"), nullable=False),
        sa.Column("client", sa.Text, nullable=False),
        sa.Column("total_cost", sa.Float, nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("note", sa.Text, nullable=True),
        sa.Column("discount", sa.Integer, nullable=True),
        sa.Column("delivered", sa.Boolean, nullable=False),
        sa.Column("date_delivered", sa.Date, nullable=True),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )



def upgrade() -> None:
    create_order_product_table()


def downgrade() -> None:
    op.drop_table("order_product")
