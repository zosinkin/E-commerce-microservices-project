from core.settings import Settings

class ShopSettings(Settings):
    REDIS_URL: str
    RABBITMQ_URL: str
    


settings = ShopSettings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}