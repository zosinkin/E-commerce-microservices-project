"""Роутеры для пользователей"""
from fastapi import APIRouter, Depends, Response
from app.dependencies import get_current_user, make_session
from app.schemas.user import UserResponseSchema, UserUpdateSchema
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])




@router.get("/me", response_model=UserResponseSchema)
async def get_me(
    current_user: User = Depends(get_current_user)
    ):
    return current_user



@router.patch("/update/", response_model=UserResponseSchema)
async def update_me(
    response: Response,
    data: UserUpdateSchema,
    session: AsyncSession = Depends(make_session),
    
    current_user: User = Depends(get_current_user),
):
    return await UserService.update_user(response=response, user=current_user, data=data, sesison=session)