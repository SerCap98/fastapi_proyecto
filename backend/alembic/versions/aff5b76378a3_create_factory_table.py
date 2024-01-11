"""create FACTORY table

Revision ID: aff5b76378a3
Revises: 949e27a284e9
Create Date: 2024-01-11 15:00:59.363991

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'aff5b76378a3'
down_revision = '949e27a284e9'
branch_labels = None
depends_on = None

def create_factory_table():
    op.create_table(
        "factory",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("identifier", sa.Text, nullable=False,unique=True),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )


def upgrade() -> None:
    create_factory_table()


def downgrade() -> None:
    op.drop_table("factory")
