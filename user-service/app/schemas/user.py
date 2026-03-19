from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
import re
from uuid import UUID


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str 
    fullname: Optional[str] = None


    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, email):
        regexp_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if (re.match(regexp_email, email) is None):
            raise ValueError(f"Неверный адрес электронной почты!")
        return email
    

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, password):
        regexp_pass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$'

        if not isinstance(password, str):
            raise ValueError("Пароль должен быть строкой")

        if len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов.")

        if re.fullmatch(regexp_pass, password) is None:
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву, "
                "одну строчную, цифру и спецсимвол."
            )

        return password



class UserResponseSchema(BaseModel):
    email: EmailStr
    fullname: Optional[str] = None
    is_active: bool
    created_at: datetime
    is_seller: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    fullname: str | None = None
    is_active: bool | None = None
    is_seller: bool | None = None



