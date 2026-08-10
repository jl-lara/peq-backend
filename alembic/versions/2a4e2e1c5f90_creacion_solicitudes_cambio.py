"""creacion solicitudes cambio

Revision ID: 2a4e2e1c5f90
Revises: 8b7d4c1a2f6e
Create Date: 2026-08-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2a4e2e1c5f90'
down_revision: Union[str, Sequence[str], None] = '8b7d4c1a2f6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'solicitudes_cambio',
        sa.Column('id_solicitud_cambio', sa.Integer(), nullable=False),
        sa.Column('id_usuario_solicita', sa.Integer(), nullable=False),
        sa.Column('id_usuario_objetivo', sa.Integer(), nullable=True),
        sa.Column('campo_afectado', sa.String(length=100), nullable=False),
        sa.Column('valor_anterior', sa.Text(), nullable=True),
        sa.Column('valor_nuevo', sa.Text(), nullable=True),
        sa.Column('motivo', sa.Text(), nullable=True),
        sa.Column('id_estado', sa.Integer(), nullable=False),
        sa.Column('fecha_solicitud', sa.DateTime(), nullable=False),
        sa.Column('fecha_revision', sa.DateTime(), nullable=True),
        sa.Column('id_revisor', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['id_estado'], ['estados.id_estado']),
        sa.ForeignKeyConstraint(['id_revisor'], ['usuarios.id_usuario']),
        sa.ForeignKeyConstraint(['id_usuario_objetivo'], ['usuarios.id_usuario']),
        sa.ForeignKeyConstraint(['id_usuario_solicita'], ['usuarios.id_usuario']),
        sa.PrimaryKeyConstraint('id_solicitud_cambio'),
    )


def downgrade() -> None:
    op.drop_table('solicitudes_cambio')
