from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base, int_pk, price, foreign_uuid
from enum import Enum




class OrderStatus(str, Enum):
    CREATED = 'CREATED'
    CONFIRMED = 'CONFIRMED'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class PymentStatus(str, Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'
    PERTIALLY_REFUNDED = 'PERTIALLY_REFUNDED'


class DeliveryStatus(str, Enum):
    PENDING = 'PENDING'
    PACKING = 'PACKING'
    SHIPPED = 'SHIPPED'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'
    RETURNED = 'RETURNED'    
    

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int_pk]
    user_id: Mapped[foreign_uuid]
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.CREATED)
    total_price: Mapped[price]
    payment_status: Mapped[PymentStatus] = mapped_column(default=PymentStatus.PENDING)
    delivery_status: Mapped[DeliveryStatus] = mapped_column(default=DeliveryStatus.PENDING)
    