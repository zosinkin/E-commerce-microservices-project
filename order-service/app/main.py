from fastapi import FastAPI
from app.routers.order import router as order_router


app = FastAPI(
    title="Order Service",
    description="Service for managing orders"
)

app.include_router(order_router)

@app.get("/")
async def root():
    return {"message": "Order Service"}

@app.get("/health")
async def health():
    return {"status": "OK"}