import httpx
from fastapi import HTTPException, Request, Response
from app.config import settings


SERVICE_MAP = {
    "user-service": settings.USER_SERVICE_URL,
    "product-service": settings.PRODUCT_SERVICE_URL,
    "order-service": settings.ORDER_SERVICE_URL,
    "seller-service": settings.SELLER_SERVICE_URL
}



async def forward_request(
    request: Request,
    service_name: str,
    path: str,
    client: httpx.AsyncClient,
) -> Response:
    """Функция для проксирования запросов к микросервисам"""
    base_url = SERVICE_MAP[service_name]
    target_url = f"{base_url}{path}"

    headers = dict(request.headers)
    headers.pop("host", None)

    body = await request.body()

    try:
        upstream_response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.query_params,
            content=body,
        )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"{service_name} недоступен")
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail=f"{service_name} не ответил вовремя")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка gateway: {str(e)}")
    
    excluded_headers = {
        "content-encoding",
        "transfer-encoding",
        "connection",
    }

    response_headers = {
        key: value
        for key, value in upstream_response.headers.items()
        if key.lower() not in excluded_headers
    }

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=response_headers,
        media_type=upstream_response.headers.get("content-type")
    )
    