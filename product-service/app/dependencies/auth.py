from fastapi import Depends, HTTPException, status, Request
from app.config import settings
from core.auth import decode_jwt_token


async def get_token(request: Request) -> str:
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found"
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
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
    return token_data
    