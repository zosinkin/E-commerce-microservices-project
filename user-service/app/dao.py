from core.dao import BaseDAO
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_by_email(cls, email: str, session: AsyncSession) -> User:
        stmt = select(cls.model).filter(cls.model.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

        
    
        
        

