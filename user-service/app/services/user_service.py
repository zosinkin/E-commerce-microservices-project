from core.auth import get_password_hash, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Response
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserUpdateSchema
from app.dao import UserDAO



class UserService:
    """Сервис для управления пользователями"""

    @classmethod
    async def create_user(cls, data: UserCreateSchema, session: AsyncSession) -> User:
        data = data.model_dump()
        exists_user = await UserDAO.get_user_by_email(session=session, email=data.get("email"))
        if exists_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
        hashed_password = await get_password_hash(data.get("password"))
        data["hashed_password"] = hashed_password
        del data["password"]
        new_user = await UserDAO.add(session=session, **data)
        return new_user
    

    @classmethod
    async def get_user_by_id(cls, id: int, session: AsyncSession) -> User:
        user = await UserDAO.get_object_by_id(session=session, obj_id=id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user
    

    @classmethod
    async def update_user(cls, response: Response, user: User, data: UserUpdateSchema, sesison: AsyncSession):
        data = data.model_dump()

        result = await UserDAO.update_data(obj_id=user.id, data=data, session=sesison)
        
        access_token = await create_access_token({
                "sub": str(user.id),
                "is_seller": user.is_seller,
                "email": user.email
                })
        response.set_cookie(key="user_access_token", value=access_token, httponly=True)
        return result
    

        
    
        
        
        

        

    