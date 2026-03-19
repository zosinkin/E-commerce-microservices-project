from fastapi import APIRouter, Depends
from app.schemas.shop import ShopCreateSchema, ShopUpdateSchema
from app.dependencies.database import make_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user
from app.services.shop_service import ShopService 



router = APIRouter(prefix="/shop", tags=["Shop"])


@router.post("/create")
async def create_shop(
    data: ShopCreateSchema,
    session: AsyncSession = Depends(make_session),
    current_user=Depends(get_current_user)
    ):
    return await ShopService.create_shop(current_user=current_user, session=session, data=data)


@router.patch("/update")
async def update_shop(
    data: ShopUpdateSchema,
    session: AsyncSession = Depends(make_session),
    current_user=Depends(get_current_user)
):
    return await ShopService.update_shop(session=session, data=data, current_user=current_user)


