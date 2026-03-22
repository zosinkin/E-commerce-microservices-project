"""
async def consume():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        name="events",
        type=aio_pika.ExchangeType.TOPIC,
        durable=True
    )

    buyer_queue = await channel.declare_queue(
        name="notification.order.created.buyer",
        durable=True
    )

    seller_queue = await channel.declare_queue(
        name="notification.order.created.seller",
        durable=True
    )

    seller_queue = await channel.declare_queue(
        "notification.order.created.seller",
        durable=True
    )

    await buyer_queue.bind(exchange=exchange, routing_key="order.created.buyer")
    await seller_queue.bind(exchange=exchange, routing_key="order.created.seller")

    await buyer_queue.consume(handle_buyer_message)
    await seller_queue.consume(handle_seller_message)

    return connection
    
"""
