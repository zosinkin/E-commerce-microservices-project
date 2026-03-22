"""Роутеры для пользователей"""
from fastapi import APIRouter, Depends, Response, status
from app.dependencies import get_current_user, make_session
from app.schemas.user import UserResponseSchema, UserUpdateSchema, UserAuthSchema, UserCreateSchema
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreateSchema,
    session: AsyncSession = Depends(make_session),
    ):
    """User registration"""
    return await UserService.create_user(session=session, data=data)


@router.post("/login", response_model=dict)
async def auth_user(
    response: Response,
    data: UserAuthSchema,
    session: AsyncSession = Depends(make_session)
):
    """User authentication"""
    return await UserService.authenticate_user(response=response, data=data, session=session)


@router.get("/me", response_model=UserResponseSchema)
async def get_me(
    current_user: User = Depends(get_current_user)
    ):
    """Getting information abbout yourself"""
    return current_user


@router.patch("/update/", response_model=UserResponseSchema)
async def update_me(
    response: Response,
    data: UserUpdateSchema,
    session: AsyncSession = Depends(make_session),
    current_user: User = Depends(get_current_user),
):
    """Update current user info"""
    return await UserService.update_user(response=response, user=current_user, data=data, sesison=session)


@router.post("/logout/", response_model=dict)
async def logout_user(response: Response):
    """User logout"""
    response.delete_cookie(key="user_access_token")
    return {"message": "User successfully logged out"}
    
    
    
