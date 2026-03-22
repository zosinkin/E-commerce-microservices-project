from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_URL: str
    SMTP_EMAIL: str
    SMTP_APP_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()