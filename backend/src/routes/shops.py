from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.shops import ShopService
from src.schemas.shops import ShopInputModel, ShopOutputModel

shop_router = APIRouter()
shop_service = ShopService()


@shop_router.get("/", response_model=List[ShopOutputModel])
async def get_all_shops(session: AsyncSession = Depends(get_session)):
    shop = await shop_service.get_all_shops(session)
    return shop


@shop_router.get("/{shop_id}", response_model=ShopOutputModel) 
async def get_shop(shop_id: str, session: AsyncSession = Depends(get_session)):
    shop = await shop_service.get_shop_by_id(shop_id, session)
    
    if shop:
        return shop
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with shop id {shop_id} not found.") 



@shop_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ShopOutputModel,
)
async def create_a_shop(
    shop_data: ShopInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await shop_service.create_shop(shop_data, session)
    except Exception as error:
        raise error



@shop_router.patch("/{shop_id}", response_model=ShopOutputModel)
async def update_shop(
    shop_id: str,
    update_data: ShopInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_shop = await shop_service.update_shop(shop_id, update_data, session)

    if updated_shop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with shop id {shop_id} not found.") 
    else:
        return updated_shop


@shop_router.delete(
    "/{shop_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_shop(shop_id: str, session: AsyncSession = Depends(get_session)):
    shop_to_delete = await shop_service.delete_shop(shop_id, session)
    
    if shop_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with shop id {shop_id} not found.") 
