"""create materia_prima table

Revision ID: 39fea22c2747
Revises: 492eec39b72d
Create Date: 2023-12-28 14:37:46.272417

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '39fea22c2747'
down_revision = '492eec39b72d'
branch_labels = None
depends_on = None

def create_materias_primas_table():
    op.create_table(
        "materias_primas",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("nombre", sa.String(100), unique=True, nullable=False),
        sa.Column("codigo", sa.String(50), unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

def upgrade() -> None:
    create_materias_primas_table()

def downgrade() -> None:
    op.drop_table("materias_primas")