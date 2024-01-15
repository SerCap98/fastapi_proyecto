"""create RAW_MATERIAL_ORDER table

Revision ID: 548765eea08d
Revises: 7ce31c7995b9
Create Date: 2024-01-11 15:03:14.583081

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

state1 = sa.Enum('APPROVED', 'REFUSED','ON HOLD', name='state1')
# revision identifiers, used by Alembic.
revision = '548765eea08d'
down_revision = '7ce31c7995b9'
branch_labels = None
depends_on = None


def create_raw_material_order_table():
    op.create_table(
        "raw_material_order",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("id_raw_material", UUID, sa.ForeignKey("raw_material.id"), nullable=False),
        sa.Column("id_factory", UUID, sa.ForeignKey("factory.id"), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("state", state1, nullable=False),
        sa.Column("note", sa.Text, nullable=True),
        sa.Column("cost", sa.Float, nullable=False),
        sa.Column("delivered", sa.Boolean, nullable=False),
        sa.Column("date_delivered", sa.Date, nullable=True),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )


def upgrade() -> None:
    create_raw_material_order_table()


def downgrade() -> None:
    op.drop_table("raw_material_order")