from pydantic import BaseModel, field_validator
from app.models.order import OrderStatus, PymentStatus, DeliveryStatus
from decimal import Decimal
from fastapi import HTTPException, status
from uuid import UUID

class OrderSchema(BaseModel):
    user_id: UUID
    status: OrderStatus
    total_price: Decimal
    payment_status: PymentStatus
    delivery_status: DeliveryStatus


class OrderResponseSchema(OrderSchema):
    id: UUID
    
    

class OrderItemCreateSchema(BaseModel):
    product_id: UUID
    quantity: int

    @field_validator("quantity", mode="before")
    @classmethod
    def validate_quantity(cls, qty):
        if qty <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Количесто товаров не может быть 0 (или меньше нуля)"
            )
        return qty


class OrderCreateSchema(BaseModel):
    items: list[OrderItemCreateSchema]

