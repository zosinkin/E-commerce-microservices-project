from fastapi import FastAPI
from app.routers.order import router as order_router
from app.dependencies.rabbitmq import rabbitmq


async def lifespan(app: FastAPI):
    await rabbitmq.connect()
    app.state.rabbitmq = rabbitmq
    yield
    await rabbitmq.close()


app = FastAPI(
    title="Order Service",
    description="Service for managing orders",
    lifespan=lifespan
)

app.include_router(order_router)


@app.get("/")
async def root():
    return {"message": "Order Service"}


@app.get("/health")
async def health():
    return {"status": "OK"}