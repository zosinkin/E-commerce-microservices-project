from core.dao import BaseDAO
from app.models.product import Product
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError


class ProductDAO(BaseDAO):
    model = Product


    @classmethod
    async def reserve_products(cls, product_list: List[Dict], session: AsyncSession) -> List[Product]:
        updated_products = []
        for product in product_list:

            product_id = product.get("id")
            qty = product.get("quantity")

            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one()
            product.stock -= qty
            updated_products.append(product)
        
        try:
            await session.commit()
          
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        
        return updated_products
        

         
