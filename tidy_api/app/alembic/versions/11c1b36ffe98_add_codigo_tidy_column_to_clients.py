from alembic import op
import sqlalchemy as sa

# Revisão ID e ID da revisão anterior
revision = '11c1b36ffe98'
down_revision = '791bb8cb3706'
branch_labels = None
depends_on = None

def upgrade():
    # Verifica se a coluna 'codigo_tidy' já existe antes de adicioná-la
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [column['name'] for column in inspector.get_columns('clients')]
    
    if 'codigo_tidy' not in columns:
        op.add_column('clients', sa.Column('codigo_tidy', sa.String(), nullable=True))

def downgrade():
    # Verifica se a coluna 'codigo_tidy' existe antes de removê-la
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [column['name'] for column in inspector.get_columns('clients')]
    
    if 'codigo_tidy' in columns:
        op.drop_column('clients', 'codigo_tidy')