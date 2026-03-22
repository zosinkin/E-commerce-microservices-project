from decimal import Decimal
from sqlalchemy import Numeric, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base, int_pk, name_str, description, foreign_uuid


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int_pk]
    name: Mapped[name_str]
    description: Mapped[description]
    shop_id: Mapped[foreign_uuid]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


    