from app.dao import OrderDAO
from app.schemas.order import OrderCreateSchema, OrderResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.clients.product_client import ProductClient
from app.models.order import OrderStatus, Order
from decimal import Decimal
from core.auth import TokenSchema



class OrderService:
    @classmethod
    async def create_order(cls, currrent_user: TokenSchema, data: OrderCreateSchema, session: AsyncSession) -> Order:
        data = data.model_dump()
        reserve_payload = []
        
        for item in data["items"]:
            payload = {
                "product_id": str(item["product_id"]),
                "quantity": item["quantity"]
            }
            reserve_payload.append(payload)
        print(data)
        
        reserved_product = await ProductClient.reserve_products(
            order_id="",
            items=reserve_payload
        )
        
        total_price = sum(Decimal(str(item["price"])) * int(item["quantity"]) for item in reserved_product)

        order = await OrderDAO.add(
            session=session,
            user_id=currrent_user.user_id,
            total_price=total_price,
            status=OrderStatus.CREATED
        )
        
        print(f"ВЫВОД: {order}")
        return order


        