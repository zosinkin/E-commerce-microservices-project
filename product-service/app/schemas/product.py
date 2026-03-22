from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, EmailStr
from fastapi import HTTPException, status
from uuid import UUID


class ProductCreateSchema(BaseModel):
    shop_id: UUID
    name: str
    description: str | None = None
    price: Decimal
    stock: int = 0


    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Стоимость не может быть меньше нуля"
            )
        return price
    
    @field_validator("stock", mode="before")
    @classmethod
    def validate_stock(cls, stock):
        if stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Количество не может быть меньше нуля"
            )
        return stock
    
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, name):
        if len(name) < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Название товара должно быть не более 255 символов."
            )
        return name
    

class ProductUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductResponseSchema(BaseModel):
    id: UUID
    name: str
    shop_id: UUID
    description: str | None
    price: Decimal
    stock: int
    is_active: bool

    model_config = {"from_attributes": True}  


class ReserveResponseSchema(BaseModel):
    id: UUID
    quantity: int
    name: str
    price: Decimal
    shop_id: UUID


class ReserveRequestSchema(BaseModel):
    id: UUID
    quantity: int



