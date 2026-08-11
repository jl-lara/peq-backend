"""merge heads

Revision ID: ef1ae9e0b021
Revises: 2a4e2e1c5f90, 758e7080ea32
Create Date: 2026-08-10 18:19:31.202948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef1ae9e0b021'
down_revision: Union[str, Sequence[str], None] = ('2a4e2e1c5f90', '758e7080ea32')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
