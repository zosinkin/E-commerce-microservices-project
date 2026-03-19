from fastapi import FastAPI
from app.routers.auth import router as auth_router 
from app.routers.users import router as user_router 


app = FastAPI(
    title="User service",
    description="User management and authentication service"
)


@app.get("/")
async def root():
    return {"message": "User service"}

app.include_router(auth_router)
app.include_router(user_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)