from core.auth import check_password, create_access_token
from app.schemas.auth import UserAuthSchema
from app.dao import UserDAO
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Response


class AuthService:

    @classmethod
    async def authenticate_user(cls, response: Response, data: UserAuthSchema, session: AsyncSession):

        user = await UserDAO.get_user_by_email(email=data.email, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный email"
            )
        if await check_password(plain_password=data.password, hashed_password=user.hashed_password) == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный пароль"
            )
        
        access_token = await create_access_token({
            "sub": str(user.id),
            "is_seller": user.is_seller,
            "email": user.email
            })
        response.set_cookie(key="user_access_token", value=access_token, httponly=True)
        return {'access_token': access_token, 'refresh_token': None}
        
