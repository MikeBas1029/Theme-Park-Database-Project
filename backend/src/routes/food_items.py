from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.food_items import FoodItemService
from src.schemas.food_items import FoodItemsInputModel, FoodItemsOutputModel

food_item_router = APIRouter()
food_item_service = FoodItemService()


@food_item_router.get("/", response_model=List[FoodItemsOutputModel])
async def get_all_food_items(session: AsyncSession = Depends(get_session)):
    food_item = await food_item_service.get_all_food_items(session)
    return food_item


@food_item_router.get("/{food_item_id}", response_model=FoodItemsOutputModel) 
async def get_food_item(food_item_id: str, session: AsyncSession = Depends(get_session)):
    food_item = await food_item_service.get_food_by_id(food_item_id, session)
    
    if food_item:
        return food_item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"FoodItem with food_item {food_item_id} not found.") 



@food_item_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FoodItemsOutputModel,
)
async def create_a_food_item(
    food_item_data: FoodItemsInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await food_item_service.create_food_item(food_item_data, session)
    except Exception as error:
        raise error



@food_item_router.patch("/{food_item_id}", response_model=FoodItemsOutputModel)
async def update_food_item(
    food_item_id: str,
    update_data: FoodItemsInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_food_item = await food_item_service.update_food_item(food_item_id, update_data, session)

    if updated_food_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"FoodItem with food_item {food_item_id} not found.") 
    else:
        return updated_food_item


@food_item_router.delete(
    "/{food_item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_food_item(food_item_id: str, session: AsyncSession = Depends(get_session)):
    food_item_to_delete = await food_item_service.delete_food_item(food_item_id, session)
    
    if food_item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"FoodItem with food_item {food_item_id} not found.") 
