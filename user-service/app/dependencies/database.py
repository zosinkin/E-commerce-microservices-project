from app.config import async_session_factory



async def make_session():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.aclose()



