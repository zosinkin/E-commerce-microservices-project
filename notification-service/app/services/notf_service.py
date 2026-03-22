import json
import aio_pika
from app.schemas.events import OrderCreatedSellerEvent, OrderCreatedBuyerEvent
from app.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio


class NotificationService:

    @classmethod
    def send_email(cls, to_email: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = to_email

        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(settings.SMTP_EMAIL, settings.SMTP_APP_PASSWORD)
            server.send_message(msg)

    @classmethod
    async def send_email_async(cls, to_email: str, subject: str, body: str):
        await asyncio.to_thread(cls.send_email, to_email, subject, body)


    @classmethod
    async def handle_seller_message(cls, message: aio_pika.IncomingMessage):
        async with message.process():
            payload = json.loads(message.body.decode("utf-8"))
            event = OrderCreatedSellerEvent.model_validate(payload)

            items_text = "\n".join(
                [
                    f"- {item.product_name}: {item.quantity} шт. × {item.price} = {item.total_price}"
                    for item in event.items
                ]
            )
            body = (
                f"Здравствуйте!\n\n"
                f"Поступил новый заказ.\n"
                f"Заказ №{event.order_id}\n"
                f"Магазин: {event.shop_id}\n"
                f"Сумма: {event.shop_total}\n\n"
                f"Товары:\n{items_text}\n"
            )

            await cls.send_email_async(
                to_email=event.seller_email,
                subject=f"Новый заказ №{event.order_id}",
                body=body
            )


    @classmethod
    async def handle_buyer_message(cls, message: aio_pika.IncomingMessage):
        async with message.process():
            payload = json.loads(message.body.decode("utf-8"))
            event = OrderCreatedBuyerEvent.model_validate(payload)

            items_text = "\n".join(
                [
                    f"- {item.product_name}: {item.quantity} шт. × {item.price}"
                    for item in event.items
                ]
            )

            body = (
                f"Здравствуйте!\n\n"
                f"Ваш заказ успешно создан.\n"
                f"Заказ №{event.order_id}\n"
                f"Статус: {event.status}\n"
                f"Сумма: {event.total_price}\n\n"
                f"Товары:\n{items_text}\n"
            )

            await cls.send_email_async(
                to_email=event.buyer_email,
                subject=f"Ваш заказ №{event.order_id}",
                body=body
            )