from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
from typing import AsyncGenerator

engine = create_async_engine(settings.DB_URL, echo=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def make_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session