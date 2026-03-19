from fastapi import FastAPI
from app.routers.shop import router as shop_router



app = FastAPI(
    title="Shop Service",
    description="Service for managing shops"
)

app.include_router(shop_router)



@app.get("/")
async def root():
    return {"message": "Seller Service"}


@app.get("/health")
async def health():
    return {"status": "OK"}