import httpx
from fastapi import HTTPException, status
from app.config import settings
from typing import List


class ProductClient:
    @classmethod
    async def reserve_products(cls, order_id: int, items: List[dict]):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.BASE_URL}/api/v1/products/reserve",
                json={
                    "order_id": str(order_id),
                    "items": items
                },
                timeout=10.0
            )
        if response.status_code != 200:
            try:
                error_data = response.json()
                detail = error_data.get("detail", "Ошибка резервирования товара")
            except Exception:
                detail = f"Ошибка резервирования товара. Status: {response.status_code}"

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
        return response.json()