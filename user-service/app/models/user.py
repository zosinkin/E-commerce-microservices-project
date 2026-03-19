from core.database import Base, int_pk, name_str, email
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users" 

    id: Mapped[int_pk]
    email: Mapped[email]
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_seller: Mapped[bool] = mapped_column(Boolean, default=False)




