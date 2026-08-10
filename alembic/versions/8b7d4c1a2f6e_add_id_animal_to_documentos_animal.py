"""add id_animal to documentos_animal

Revision ID: 8b7d4c1a2f6e
Revises: cf0c580de35b
Create Date: 2026-08-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8b7d4c1a2f6e'
down_revision: Union[str, Sequence[str], None] = 'cf0c580de35b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('documentos_animal', sa.Column('id_animal', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'documentos_animal_id_animal_fkey',
        'documentos_animal',
        'animal',
        ['id_animal'],
        ['id_animal'],
    )


def downgrade() -> None:
    op.drop_constraint('documentos_animal_id_animal_fkey', 'documentos_animal', type_='foreignkey')
    op.drop_column('documentos_animal', 'id_animal')