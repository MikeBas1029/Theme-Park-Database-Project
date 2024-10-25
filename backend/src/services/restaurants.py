from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.restaurants import Restaurants
from src.schemas.restaurants import RestaurantInputModel


class RestaurantService:
    async def get_all_restaurants(self, session: AsyncSession):
        query = select(Restaurants)

        result = await session.exec(query)

        return result.all()
    
    async def get_restaurant_by_id(self, restaurant_id: str, session: AsyncSession):
        query = select(Restaurants).where(Restaurants.restaurant_id == restaurant_id)

        result = await session.exec(query)

        restaurant = result.first()

        return restaurant if restaurant is not None else None 
    
    async def restaurant_exists(self, restaurant_id: str, session: AsyncSession):
        query = select(Restaurants).where(Restaurants.restaurant_id == restaurant_id)

        result = await session.exec(query)

        restaurant = result.first()

        return bool(restaurant)
    
    async def create_restaurant(
            self,
            restaurant_data: RestaurantInputModel,
            session: AsyncSession
    ):
        restaurant_data_dict = restaurant_data.model_dump()

        new_restaurant = Restaurants(**restaurant_data_dict)

        # First check if restaurant exists already
        existing_restaurant = await self.restaurant_exists(new_restaurant.restaurant_id, session)

        if existing_restaurant:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Restaurant with restaurant_id {new_restaurant.restaurant_id} already exists.")
        else:
            session.add(new_restaurant)

            await session.commit()

            return new_restaurant
    

    async def update_restaurant(
            self, 
            restaurant_id: str,
            update_data: RestaurantInputModel,
            session: AsyncSession
    ):
        restaurant_to_update = await self.get_restaurant_by_id(restaurant_id, session)


        if restaurant_to_update is not None:
            restaurant_update_dict = update_data.model_dump()

            for k, v in restaurant_update_dict.items():
                setattr(restaurant_to_update, k, v)

            await session.commit()

            return restaurant_to_update
        else:
            return None  
        
    async def delete_restaurant(self, restaurant_id: str, session: AsyncSession):
        restaurant_to_delete = await self.get_restaurant_by_id(restaurant_id, session)

        if restaurant_to_delete is not None:
            await session.delete(restaurant_to_delete)
            await session.commit()

            return {}
        else:
            return None