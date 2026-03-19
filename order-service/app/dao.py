from core.dao import BaseDAO
from app.models.order import Order

class OrderDAO(BaseDAO):
    model = Order