from core.dao import BaseDAO
from app.models.order import Order, OrderItem


class OrderDAO(BaseDAO):
    model = Order


class OrderItemDAO(BaseDAO):
    model = OrderItem