from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True  # Для SQLAlchemy 2.0+
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True  # Для SQLAlchemy 2.0+
)

Base = declarative_base()

async def get_async_session():
    async with async_session_maker() as session:
        yield session
