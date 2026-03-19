from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from app.auth import authenticate_request

from app.proxy import forward_request
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    unexpected_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=10.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="API Gateway",
    description="Gateway for e-commerce microservices",
    lifespan=lifespan,
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unexpected_exception_handler)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    await authenticate_request(request)
    return await call_next(request)



@app.get("/")
async def root():
    return {"message": "API Gateway"}


@app.get("/health")
async def health():
    return {"status": "ok"}



"""Проксирование User-service"""
@app.api_route("/api/v1/auth/register", methods=["POST"])
async def register(request: Request):
    return await forward_request(
        request=request,
        service_name="user-service",
        path="/api/v1/auth/register",
        client=request.app.state.http_client,
    )


@app.api_route("/api/v1/auth/login", methods=["POST"])
async def login(request: Request):
    return await forward_request(
        request=request,
        service_name="user-service",
        path="/api/v1/auth/login",
        client=request.app.state.http_client,
    )


@app.api_route("/api/v1/users/me", methods=["GET"])
async def get_me(request: Request):
    return await forward_request(
        request=request,
        service_name="user-service",
        path="/api/v1/users/me",
        client=request.app.state.http_client,
    )



"""Проксирование Product-service"""
@app.api_route("/api/v1/products", methods=["GET"])
async def get_products(request: Request):
    return await forward_request(
        request=request,
        service_name="product-service",
        path="/api/v1/products",
        client=request.app.state.http_client,
    )


@app.api_route("/api/v1/products/create", methods=["POST"])
async def create_porduct(request: Request):
    return await forward_request(
        request=request,
        service_name="product-service",
        path="/api/v1/products/create",
        client=request.app.state.http_client,
    )


@app.api_route("/api/v1/products/reserve", methods=["POST"])
async def reserve_products(request: Request):
    return await forward_request(
        request=request,
        service_name="product-service",
        path="/api/v1/products/reserve",
        client=request.app.state.http_client
    )


@app.api_route("/api/v1/products/{product_id}", methods=["GET"])
async def product_detail(request: Request, product_id: int):
    return await forward_request(
        request=request,
        service_name="product-service",
        path=f"/api/v1/products/{product_id}",
        client=request.app.state.http_client,
    )


@app.api_route("/api/v1/products/update/{product_id}", methods=["PUTCH"])
async def upadte_product(request: Request, product_id: int):
    return await forward_request(
        request=request,
        service_name="product-service",
        path=f"/api/v1/products/update/{product_id}"
    )


"""Проксирование Order-service"""
@app.api_route("/order/create", methods=["POST"])
async def create_order(request: Request):
    return await forward_request(
        request=request,
        service_name="order-service",
        path="/order/create",
        client=request.app.state.http_client,
    )


"""Проксирование Seller-service"""
@app.api_route("/seller/create", methods=["POST"])
async def create_seller(request: Request):
    return await forward_request(
        request=request,
        service_name="seller-service",
        path="/seller/create",
        client=request.app.state.http_client,
    )


@app.api_route("/seller/update", methods=["PUTCH"])
async def update_seller(request: Request):
    return await forward_request(
        request=request,
        service_name="seller-service",
        path="/seller/update",
        client=request.app.state.http_client,
    )


@app.api_route("/shop/create", methods=["POST"])
async def create_shop(request: Request):
    return await forward_request(
        request=request,
        service_name="seller-service",
        path="/shop/create",
        client=request.app.state.http_client,
)


@app.api_route("/shop/update", methods=["PUTCH"])
async def update_shop(request: Request):
    return await forward_request(
    request=request,
    service_name="seller-service",
    path="/shop/update",
    client=request.app.state.http_client,
)