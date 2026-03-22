from core.config import Settings


class ProductSettings(Settings):
    REDIS_URL: str
    RABBITMQ_URL: str

settings = ProductSettings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
