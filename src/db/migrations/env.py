import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# Импортируем Base и все модели
from src.db.base import Base
from src.accounts import models as accounts_models
from src.movies import models as movies_models
from src.orders import models as orders_models
from src.cart import models as cart_models
from src.payments import models as payments_models
from src.core.config import settings  # 🔹 Используем конфиг проекта

# Настройка логгирования
config = context.config
fileConfig(config.config_file_name)

# Метаданные всех моделей
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = settings.db_url  # 💡 Используем конфигурацию из settings
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(settings.db_url, future=True)  # 🔹 settings.db_url

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
