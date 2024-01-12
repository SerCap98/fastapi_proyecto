"""create BACKLOG table

Revision ID: 6196e3b31033
Revises: 015f4d6c69e6
Create Date: 2024-01-11 15:05:46.623464

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '6196e3b31033'
down_revision = '015f4d6c69e6'
branch_labels = None
depends_on = None

state2 = sa.Enum('ATTENDED', 'PENDING', name='state2')

def create_backlog_table():
    op.create_table(
        "backlog",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("id_order_product", UUID, sa.ForeignKey("order_product.id"), nullable=False),
        sa.Column("missing_amount", sa.Integer, nullable=False),
        sa.Column("state", state2, nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_backlog_table()

def downgrade() -> None:
    op.drop_table("backlog")