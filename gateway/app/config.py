from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):

    USER_SERVICE_URL: str
    PRODUCT_SERVICE_URL: str
    ORDER_SERVICE_URL:str 
    SELLER_SERVICE_URL: str
    
    SECRET_KEY: str
    ALGORITHM: str

    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = 'allow'

settings = Settings()