from fastapi import FastAPI
from app.routers.users import router as user_router 


app = FastAPI(
    title="User service",
    description="User management and authentication service"
)


@app.get("/")
async def root():
    return {"message": "User service"}


app.include_router(user_router)


@app.get("/health")
async def health():
    return {"message": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)