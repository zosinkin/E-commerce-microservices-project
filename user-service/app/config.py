from core.config import Settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


engine = create_async_engine(settings.DB_URL)
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
    )


