from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from app.models.shop import ShopStatus


class TokenSchema(BaseModel):
    user_id: UUID
    email: EmailStr 
    is_seller: bool


class ShopCreateSchema(BaseModel):
    name: str
    description: str
   

class ShopUpdateSchema(BaseModel):
    id: UUID
    name: str | None = None
    description: str | None = None
    status: ShopStatus | None = None



