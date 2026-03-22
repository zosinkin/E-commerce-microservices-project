from fastapi import Depends, HTTPException, status, Request
from app.config import settings
from fastapi import Request
from core.auth import decode_jwt_token
from app.dao import UserDAO
from app.dependencies.database import make_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserResponseSchema


async def get_token(request: Request) -> str:
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found"
        )
    return token


async def get_current_user(token: str = Depends(get_token), session: AsyncSession = Depends(make_session)) -> UserResponseSchema:
    """Getting information about the authenticated user"""
    token_data = decode_jwt_token(
        token=token,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    current_user = await UserDAO.get_object_by_id(obj_id=token_data.user_id, session=session)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return current_user
    