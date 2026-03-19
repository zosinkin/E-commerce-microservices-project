from fastapi import FastAPI
import asyncio
from app.consumers.product_events import handle_product_created
from app.routers.products import router as product_router
from app.dependencies.redis import redis_client
from contextlib import asynccontextmanager
from app.events import (
    PRODUCTS_EXCHANGE,
    PRODUCT_CREATED_KEY,
    PRODUCTS_AUDIT_QUEUE
)

consumer_task: asyncio.Task | None = None



app = FastAPI(
    title="Product Service",
    description="Service for managing products",
    )

app.include_router(product_router)
 



@app.get("/")
async def root():
    return {"message": "Product Service"}


@app.get("/health")
async def health():
    return {"status": "ok"}