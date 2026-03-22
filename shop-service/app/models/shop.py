from core.database import Base
from core.database import int_pk, name_str, description, rating, slug, foreign_uuid, email
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (text, func, Integer)
from enum import Enum


class ShopStatus(Enum):
    pending = "pending"
    active = "active"
    suspended = "suspended"
    blocked = "blocked"
    deactivated = "deactivated"


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int_pk]
    name: Mapped[name_str]
    description: Mapped[description]
    slug: Mapped[slug]
    seller_id: Mapped[foreign_uuid]
    email: Mapped[email]
    is_verified: Mapped[foreign_uuid]
    status: Mapped[ShopStatus] = mapped_column(default=ShopStatus.pending, nullable=True)
    rating: Mapped[rating] 
    total_reviews: Mapped[int] = mapped_column(nullable=True, default=0, server_default=text("0"))
    total_orders: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    total_products: Mapped[int] = mapped_column(Integer, default=0, nullable=True)




