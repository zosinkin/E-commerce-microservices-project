from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from core.database import Base
from app.config import settings


engine = create_async_engine(settings.DB_URL)
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
    )


