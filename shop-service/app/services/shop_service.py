from app.schemas.shop import ShopUpdateSchema, ShopCreateSchema, TokenSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.shop import Shop
from app.dao import ShopDAO
from fastapi import HTTPException, status
from slugify import slugify 
from uuid import UUID


class ShopService:
    """Shop managing service"""
    @classmethod
    async def create_shop(cls, current_user: TokenSchema, data: ShopCreateSchema, session: AsyncSession) -> Shop:
        current_user = current_user.model_dump()
        print(current_user)
        if current_user["is_seller"] == False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="To create a shop, you need to become a seller."
            )

        data = data.model_dump()
        exist_shop = await ShopDAO.get_one_by_filter(session=session, **data)
        
        if exist_shop:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Shop with this name does not exists"
            )
        
        data["seller_id"] = current_user["user_id"]
        data["slug"] = slugify(data["name"])
        new_shop = await ShopDAO.add(session=session, **data)
        return new_shop
    

    @classmethod
    async def update_shop(cls, data: ShopUpdateSchema, session: AsyncSession, current_user: dict) -> Shop:
        data = data.model_dump()
        data["slug"] = slugify(data["name"]) 
        return await ShopDAO.update_data(obj_id=data["id"], session=session, data=data)
    

    @classmethod
    async def get_shop_info(cls, id: UUID, session: AsyncSession):
        shop = await ShopDAO.get_object_by_id(obj_id=id, session=session)

        if shop is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shop not found"
            )    
        return shop