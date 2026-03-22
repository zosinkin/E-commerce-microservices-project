from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.broker.rabbitmq import RabbitMQClient
from app.services.notf_service import NotificationService
from app.config import settings


rabbitmq = RabbitMQClient(settings.RABBITMQ_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq.connect()
    await rabbitmq.subscribe(
        queue_name="notification.order.created.buyer",
        routing_key="order.created.buyer",
        handler=NotificationService.handle_buyer_message
        )
    await rabbitmq.subscribe(
        queue_name="notification.order.created.seller",
        routing_key="order.created.buyer",
        handler=NotificationService.handle_seller_message
    )
    yield
    await rabbitmq.close()

app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}