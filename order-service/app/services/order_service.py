from app.dao import OrderDAO, OrderItemDAO
from app.schemas.order import OrderItemCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.clients.order_client import OrderClient
from app.models.order import OrderStatus, Order
from decimal import Decimal
from core.auth import TokenSchema
from typing import List
from collections import defaultdict
from app.dependencies.rabbitmq import rabbitmq


class OrderService:
    @classmethod
    async def create_order(cls, current_user: TokenSchema, data: List[OrderItemCreateSchema], session: AsyncSession) -> Order:
        data = [item.model_dump() for item in data]
        reserve_payload = []
            
        for item in data:
            reserve_payload.append({
                "id": str(item["id"]),
                "quantity": item["quantity"]
            })
        print(data)

        reserved_products = await OrderClient.reserve_products(
            items=reserve_payload
        )
        shop_emails = {}
        if reserved_products:
            unique_shop_ids = {str(item["shop_id"]) for item in reserved_products}

            for shop_id in unique_shop_ids:
                shop_info = await OrderClient.get_shop_info(id=shop_id)
                shop_emails[shop_id] = shop_info["email"]
        
        total_price = sum(Decimal(str(item["price"])) * int(item["quantity"]) for item in reserved_products)

        order = await OrderDAO.add(
            session=session,
            user_id=current_user.user_id,
            total_price=total_price,
            status=OrderStatus.CREATED
        )

        orders = []
        for item in reserved_products:
            price = Decimal(str(item["price"]))
            quantity = int(item["quantity"])

            orders.append(
                {
                    "order_id": order.id,
                    "product_id": item["id"],
                    "shop_id": item["shop_id"],
                    "product_name": item["name"],
                    "quantity": quantity,
                    "price": price,
                    "total_price": price * quantity, 
                }
            )
        
        await OrderItemDAO.add_many(
            data=orders, 
            session=session
            )
           
        buyer_message = {
            "event": "order.created.buyer",
            "order_id": str(order.id),
            "buyer_email": str(current_user.email),
            "buyer_id": str(current_user.user_id),
            "total_price": str(order.total_price),
            "status": order.status.value,
            "items": [
                {
                    "product_id": str(item["id"]),
                    "product_name": item["name"],
                    "quantity": item["quantity"],
                    "price": str(item["price"]),
                    "shop_id": str(item["shop_id"]),
                }
                for item in reserved_products
            ]
        }

        await rabbitmq.publish(
            routing_key="order.created.buyer", 
            message=buyer_message
            )
        
        grouped_by_shop = defaultdict(list)
        for item in reserved_products:
            grouped_by_shop[str(item["shop_id"])].append(item)

        for shop_id, shop_items in grouped_by_shop.items():
            shop_total = sum(
                Decimal(str(i["price"])) * int(i["quantity"])
                for i in shop_items
            )

            seller_message = {
                "event": "order.created.seller",
                "order_id": str(order.id),
                "shop_id": str(shop_id),
                "seller_email": shop_emails.get(str(shop_id)),
                "items": [
                    {
                        "product_id": str(i["id"]),
                        "product_name": i["name"],
                        "quantity": i["quantity"],
                        "price": str(i["price"]),
                        "total_price": str(
                            Decimal(str(i["price"])) * int(i["quantity"])
                        ),
                    }
                    for i in shop_items
                ],
                "shop_total": str(shop_total)
            }

            await rabbitmq.publish(
                routing_key="order.created.seller",
                message=seller_message
            )
        return order


        