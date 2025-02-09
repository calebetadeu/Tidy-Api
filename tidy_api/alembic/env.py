from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Adicione o caminho do seu aplicativo ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Importa o modelo Base do seu aplicativo
from tidy_api.app.models import Base

# Configurações do arquivo alembic.ini
config = context.config

# Interpreta a configuração do arquivo de log do .ini
fileConfig(config.config_file_name)

# Adiciona o modelo Base ao contexto do Alembic
target_metadata = Base.metadata

def run_migrations_offline():
    """Executa migrações no modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Executa migrações no modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()