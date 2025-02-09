"""Adiciona latitude e longitude

Revision ID: 791bb8cb3706
Revises: 
Create Date: 2025-02-07 09:47:27.351080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '791bb8cb3706'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Verifica se as colunas 'latitude' e 'longitude' já existem antes de adicioná-las
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [column['name'] for column in inspector.get_columns('clients')]
    
    if 'latitude' not in columns:
        op.add_column('clients', sa.Column('latitude', sa.Float(), nullable=True))
    
    if 'longitude' not in columns:
        op.add_column('clients', sa.Column('longitude', sa.Float(), nullable=True))


def downgrade() -> None:
    # Verifica se as colunas 'latitude' e 'longitude' existem antes de removê-las
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [column['name'] for column in inspector.get_columns('clients')]
    
    if 'longitude' in columns:
        op.drop_column('clients', 'longitude')
    
    if 'latitude' in columns:
        op.drop_column('clients', 'latitude')