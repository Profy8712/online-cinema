import asyncio
import os
import sys

# Установим путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from sqlalchemy.ext.asyncio import AsyncEngine
from src.db.session import async_session_maker, Base, engine
from src.accounts.enums import UserGroupEnum
from src.accounts.models import UserGroup
from sqlalchemy import select


async def init_db():
    async with engine.begin() as conn:
        # Создаём все таблицы
        await conn.run_sync(Base.metadata.create_all)

    # Добавляем дефолтную группу пользователей, если не существует
    async with async_session_maker() as session:
        for group in UserGroupEnum:
            result = await session.execute(select(UserGroup).where(UserGroup.name == group))
            if not result.scalar_one_or_none():
                session.add(UserGroup(name=group))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(init_db())
