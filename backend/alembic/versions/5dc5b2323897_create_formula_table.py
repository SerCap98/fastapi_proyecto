"""create FORMULA table

Revision ID: 5dc5b2323897
Revises: 548765eea08d
Create Date: 2024-01-11 15:03:51.477160

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID



# revision identifiers, used by Alembic.
revision = '5dc5b2323897'
down_revision = '548765eea08d'
branch_labels = None
depends_on = None

def create_formula_table():
    op.create_table(
        "formula",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("quantity", sa.Float, nullable=False),
        sa.Column("id_raw_material", UUID, sa.ForeignKey("raw_material.id"), nullable=False),
        sa.Column("id_product", UUID, sa.ForeignKey("product.id"), nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_by", UUID(as_uuid=True), nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )

def upgrade() -> None:
    create_formula_table()


def downgrade() -> None:
    op.drop_table("formula")
