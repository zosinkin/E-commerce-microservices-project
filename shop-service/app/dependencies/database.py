from app.database import engine, async_session_factory
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def make_session():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.aclose()



