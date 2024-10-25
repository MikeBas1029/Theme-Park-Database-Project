from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.restaurants import RestaurantService
from src.schemas.restaurants import RestaurantInputModel, RestaurantOutputModel

restaurant_router = APIRouter()
restaurant_service = RestaurantService()


@restaurant_router.get("/", response_model=List[RestaurantOutputModel])
async def get_all_restaurants(session: AsyncSession = Depends(get_session)):
    restaurant = await restaurant_service.get_all_restaurants(session)
    return restaurant


@restaurant_router.get("/{restaurant_id}", response_model=RestaurantOutputModel) 
async def get_restaurant(restaurant_id: str, session: AsyncSession = Depends(get_session)):
    restaurant = await restaurant_service.get_restaurant_by_id(restaurant_id, session)
    
    if restaurant:
        return restaurant
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with restaurant id {restaurant_id} not found.") 



@restaurant_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RestaurantOutputModel,
)
async def create_a_restaurant(
    restaurant_data: RestaurantInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await restaurant_service.create_restaurant(restaurant_data, session)
    except Exception as error:
        raise error



@restaurant_router.patch("/{restaurant_id}", response_model=RestaurantOutputModel)
async def update_restaurant(
    restaurant_id: str,
    update_data: RestaurantInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_restaurant = await restaurant_service.update_restaurant(restaurant_id, update_data, session)

    if updated_restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with restaurant id {restaurant_id} not found.") 
    else:
        return updated_restaurant


@restaurant_router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_restaurant(restaurant_id: str, session: AsyncSession = Depends(get_session)):
    restaurant_to_delete = await restaurant_service.delete_restaurant(restaurant_id, session)
    
    if restaurant_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with restaurant id {restaurant_id} not found.") 
