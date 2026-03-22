from pydantic import BaseModel, EmailStr
from uuid import UUID
from decimal import Decimal
from typing import List 

class SellerItem(BaseModel):
    product_id: UUID
    product_name: str
    quantity: int
    price: Decimal
    total_price: Decimal


class OrderCreatedSellerEvent(BaseModel):
    event: str
    order_id: UUID
    shop_id: UUID
    seller_email: str
    items: List[SellerItem]
    shop_total: Decimal


class BuyerItem(BaseModel):
    product_id: UUID
    product_name: str
    quantity: int
    price: Decimal
    shop_id: UUID


class OrderCreatedBuyerEvent(BaseModel):
    event: str
    order_id: UUID
    buyer_id: UUID
    buyer_email: str
    total_price: Decimal
    status: str
    items: List[BuyerItem]