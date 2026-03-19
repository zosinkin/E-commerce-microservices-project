from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema,ReserveRequestSchema
from app.dao import ProductDAO
import json
from app.schemas.product import ProductResponseSchema
from app.dependencies.redis import redis_client 
from app.events import (
    PRODUCTS_EXCHANGE,
    PRODUCT_CREATED_KEY,
    PRODUCT_UPDATED_KEY,
)
from app.config import settings


class ProductService:
    
    @classmethod
    async def create_product(cls, 
                            data: ProductCreateSchema,
                            session: AsyncSession) -> ProductResponseSchema:
        
        data = data.model_dump()
        product = await ProductDAO.add(session=session, **data)

        await redis_client.delete("products:all")

        product_data = ProductResponseSchema.model_validate(product).model_dump(mode="json")
        

        return ProductResponseSchema.model_validate(product)
    

    @classmethod
    async def get_products(cls, session: AsyncSession) -> List[dict]:
        cache_key = "products:all"

        cached_products = await redis_client.get(cache_key)
        if cached_products:
            return json.loads(cached_products)

        all_products = await ProductDAO.get_all_objects(session=session)
        if not all_products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет товаров"
            )

        all_products_data = [
            ProductResponseSchema.model_validate(product).model_dump(mode="json")
            for product in all_products
        ]

        await redis_client.set(cache_key, json.dumps(all_products_data), ex=60)
        return all_products_data


    @classmethod 
    async def get_product_by_id(cls, product_id: int, session: AsyncSession) -> dict:
        cache_key = f"products:{product_id}"

        cached_product = await redis_client.get(cache_key)
        if cached_product:
            return json.loads(cached_product)
        
        product = await ProductDAO.get_object_by_id(session=session, obj_id=product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого товара не существует"
            )
        
        product_data = (
            ProductResponseSchema
            .model_validate(product)
            .model_dump(mode="json")
            )

        await redis_client.set(cache_key, json.dumps(product_data), ex=60)
        return product_data
    

    @classmethod
    async def update_product(cls, product_id: int, data: ProductUpdateSchema, session: AsyncSession) -> ProductResponseSchema:

        update_data = data.model_dump(exclude_unset=True)

        if "price" in update_data and update_data["price"] < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Стоимость не может быть меньше нуля"
                )

        if "stock" in update_data and update_data["stock"] < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Наличие не может быть меньше нуля"
            )
        product = await ProductDAO.update_data(session=session, obj_id=product_id, data=update_data)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )

        await redis_client.delete("products:all")
        await redis_client.delete(f"products:{product_id}")

        product_data = ProductResponseSchema.model_validate(product).model_dump(mode="json")

        return ProductResponseSchema.model_validate(product)
    

    @classmethod
    async def reserve_products(cls, data: ReserveRequestSchema, session: AsyncSession) -> List[dict]:
        payload = data.model_dump()
        
        product_list = []
        for item in payload["items"]:
            product = await ProductDAO.get_object_by_id(session=session, obj_id=item["product_id"])

            if product is None:
                raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Товар {item['product_id']} не найден"
                )
            
            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Товар {item['product_id']} не активен"
                )
            
            if product.stock < item["quantity"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Недостаточно товара {item['product_id']}"
                )
            
            product_list.append({
                "id": item["product_id"],
                "quantity": item["quantity"],
                "price": product.price
            })
        
        await ProductDAO.reserve_products(product_list, session=session)
        return product_list
        
            
        
            

            
            
        
           

            
            
            
            
        
        




    