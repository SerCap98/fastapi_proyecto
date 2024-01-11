"""create ALERT table

Revision ID: 7ce31c7995b9
Revises: 5fd0bda9a45c
Create Date: 2024-01-11 15:02:55.173556

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

state2 = sa.Enum('ATTENDED', 'PENDING', name='state2')

# revision identifiers, used by Alembic.
revision = '7ce31c7995b9'
down_revision = '5fd0bda9a45c'
branch_labels = None
depends_on = None

def create_alert_table():
    op.create_table(
        "alert",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("id_factory_inventory", UUID(as_uuid=True), sa.ForeignKey("factory_raw_material_inventory.id"), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("state", state2, nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_alert_table()


def downgrade() -> None:
    op.drop_table("alert")