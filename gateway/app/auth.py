from datetime import datetime, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, Request, status

from app.config import settings


PUBLIC_PATHS = {
    "/",
    "/health",
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/products",
    "/api/v1/products/{product_id}",
}


def is_public_path(path: str) -> bool:
    return path in PUBLIC_PATHS


async def authenticate_request(request: Request):
    if is_public_path(request.url.path):
        return
    
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token not found'
        )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    exp = payload.get("exp")
    if not exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has no exp"
        )
    
    expire_time = datetime.fromtimestamp(int(exp), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User id not found in token"
        )
    
    request.state.user_id = user_id