from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_async_session():
    async with async_session_maker() as session:
        yield session
