"""Роутеры для аутентификации"""
from fastapi import APIRouter, Depends, status
from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import make_session
from app.services.user_service import UserService
from app.schemas.auth import UserAuthSchema
from fastapi import Response
from app.schemas.auth import UserAuthSchema




router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreateSchema,
    session: AsyncSession = Depends(make_session),
    ):
    return await UserService.create_user(session=session, data=data)


@router.post("/login", response_model=dict)
async def auth_user(
    response: Response,
    data: UserAuthSchema,
    session: AsyncSession = Depends(make_session)
):
    return await AuthService.authenticate_user(response=response, data=data, session=session)



@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {"message": "Пользователь успешно вышел из системы"}
    
    
    
