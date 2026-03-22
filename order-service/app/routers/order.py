from fastapi import APIRouter, Depends
from app.schemas.order import OrderItemCreateSchema, OrderResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import make_session
from app.dependencies.auth import get_current_user
from app.services.order_service import OrderService
from typing import List

router = APIRouter(prefix="/order", tags=["Orders"])


@router.post("/create", response_model=OrderResponseSchema)
async def create_order(
    data: List[OrderItemCreateSchema],
    session: AsyncSession = Depends(make_session),
    current_user=Depends(get_current_user)
):
    return await OrderService.create_order(current_user=current_user, data=data, session=session)

    

