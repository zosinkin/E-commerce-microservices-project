from core.rabbitmq import RabbitMQClient
from app.config import settings


rabbitmq = RabbitMQClient(settings.RABBITMQ_URL)

