from core.auth import get_password_hash, create_access_token, check_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Response
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserUpdateSchema, UserAuthSchema
from app.dao import UserDAO


class UserService:
    """User management service"""

    @classmethod
    async def create_user(cls, data: UserCreateSchema, session: AsyncSession) -> User:
        data = data.model_dump()
        exists_user = await UserDAO.get_user_by_email(session=session, email=data.get("email"))
        if exists_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exist"
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
                detail="User not found"
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
    

    @classmethod
    async def authenticate_user(cls, response: Response, data: UserAuthSchema, session: AsyncSession):

        user = await UserDAO.get_user_by_email(email=data.email, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong email"
            )
        if await check_password(plain_password=data.password, hashed_password=user.hashed_password) == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong password"
            )
        
        access_token = await create_access_token({
            "sub": str(user.id),
            "is_seller": user.is_seller,
            "email": user.email
            })
        response.set_cookie(key="user_access_token", value=access_token, httponly=True)
        return {'access_token': access_token, 'refresh_token': None}
        


        
    
        
        
        

        

    