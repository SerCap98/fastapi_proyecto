"""create PRODUCT table

Revision ID: 949e27a284e9
Revises: 450c129f2b3f
Create Date: 2024-01-11 15:00:37.096610

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '949e27a284e9'
down_revision = '450c129f2b3f'
branch_labels = None
depends_on = None

def create_product_table():
    op.create_table(
        "product",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("name", sa.Text, nullable=False,unique=True),
        sa.Column("cost_per_bag", sa.Float, nullable=False),        
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:  
    create_product_table()

def downgrade() -> None:
    op.drop_table("product")