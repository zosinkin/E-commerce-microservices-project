from fastapi import APIRouter, Depends, status
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema, ProductResponseSchema, ReserveResponseSchema
from app.services.product_service import ProductService
from app.dependencies.database import make_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user
from app.schemas.product import ReserveRequestSchema
from uuid import UUID
from typing import List


router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.get("", response_model= List[ProductResponseSchema])
async def get_all_products(session: AsyncSession = Depends(make_session)):
    return await ProductService.get_products(session=session)
     

@router.post("/create", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreateSchema,
    session: AsyncSession = Depends(make_session),
    current_user =  Depends(get_current_user)
    ):
    return await ProductService.create_product(session=session, data=data)


@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product(
    product_id: UUID, 
    session: AsyncSession = Depends(make_session)
    ):
    return await ProductService.get_product_by_id(product_id=product_id, session=session)


@router.patch("/update/{product_id}", response_model=ProductResponseSchema)
async def update_product(
    product_id: UUID,
    data: ProductUpdateSchema,
    session: AsyncSession = Depends(make_session),
    current_user=Depends(get_current_user)
    ):
    return await ProductService.update_product(product_id=product_id, data=data, session=session)


@router.post("/reserve", response_model=List[ReserveResponseSchema])
async def reserve_products(
    data: List[ReserveRequestSchema],
    session: AsyncSession = Depends(make_session),
    current_user=Depends(make_session)
    ):
    return await ProductService.reserve_products(data=data, session=session)

    






