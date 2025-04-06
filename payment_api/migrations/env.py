from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models import Base
import asyncio

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url")
    )

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())

run_migrations_online()
