import httpx
from fastapi import HTTPException, status
from app.config import settings
from typing import List


class OrderClient:
    @classmethod
    async def reserve_products(cls, items: List[dict]):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/reserve",
                json=items,
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
    

    @classmethod
    async def get_shop_info(cls, id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.SHOP_SERVICE_URL}/shop/{id}",
                timeout=10.0
            )
        if response.status_code != 200:
            try:
                error_data = response.json()
                detail = error_data.get("detail", "Ошибка при получении магазина")
            except Exception:
                detail = f"Ошибка получения магазина. Status: {response.status_code}"
                
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
        return response.json()

        
