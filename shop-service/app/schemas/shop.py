from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.shop import ShopStatus


class TokenSchema(BaseModel):
    user_id: UUID
    email: EmailStr 
    is_seller: bool


class ShopCreateSchema(BaseModel):
    name: str
    email: EmailStr
    description: str
   

class ShopUpdateSchema(BaseModel):
    id: UUID
    name: str | None = None
    description: str | None = None
    status: ShopStatus | None = None


class ShopResponseSchema(BaseModel):
    id: UUID
    name: str
    description: str
    status: ShopStatus
    seller_id: UUID
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)



