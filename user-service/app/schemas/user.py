from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
import re


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str 
    fullname: str | None = None


    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, email):
        regexp_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if (re.match(regexp_email, email) is None):
            raise ValueError(f"Wrong email!")
        return email
    

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, password):
        regexp_pass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$'

        if not isinstance(password, str):
            raise ValueError("Password must be a string")

        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters")

        if re.fullmatch(regexp_pass, password) is None:
            raise ValueError(
                "Password must contain at least one uppercase letter,"
                "one lowercase letter, one digit and special character."
            )
        return password


class UserResponseSchema(BaseModel):
    email: EmailStr
    fullname: str | None = None
    is_active: bool
    created_at: datetime
    is_seller: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    fullname: str | None = None
    is_active: bool | None = None
    is_seller: bool | None = None


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str
    





