from core.dao import BaseDAO
from app.models.shop import Shop
from sqlalchemy.ext.asyncio import AsyncSession


class ShopDAO(BaseDAO):
    model = Shop
    


    
