from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base, int_pk, price, foreign_uuid
from enum import Enum
from uuid import UUID
from sqlalchemy import Uuid, ForeignKey, String, Numeric
from decimal import Decimal


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



class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int_pk]
    order_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("orders.id"), nullable=False)

    product_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    shop_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)

    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)




    