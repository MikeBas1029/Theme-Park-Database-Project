from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.food_items import FoodItems
from src.schemas.food_items import FoodItemsInputModel


class FoodItemService:
    async def get_all_food_items(self, session: AsyncSession):
        query = select(FoodItems).order_by(FoodItems.food_type)

        result = await session.exec(query)

        return result.all()
    
    async def get_food_by_id(self, food_id: str, session: AsyncSession):
        query = select(FoodItems).where(FoodItems.food_id == food_id)

        result = await session.exec(query)

        food = result.first()

        return food if food is not None else None 
    
    async def food_exists(self, food_id: str, session: AsyncSession):
        query = select(FoodItems).where(FoodItems.food_id == food_id)

        result = await session.exec(query)

        food = result.first()

        return bool(food)
    
    async def create_food_item(
            self,
            food_data: FoodItemsInputModel,
            session: AsyncSession
    ):
        food_data_dict = food_data.model_dump()

        new_food = FoodItems(**food_data_dict)

        # First check if food exists already
        existing_food = await self.food_exists(new_food.food_id, session)

        if existing_food:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"FoodItem with food_id {new_food.food_id} already exists.")
        else:
            session.add(new_food)

            await session.commit()

            return new_food
    

    async def update_food_item(
            self, 
            food_id: str,
            update_data: FoodItemsInputModel,
            session: AsyncSession
    ):
        food_to_update = await self.get_food_by_id(food_id, session)


        if food_to_update is not None:
            food_update_dict = update_data.model_dump()

            for k, v in food_update_dict.items():
                setattr(food_to_update, k, v)

            await session.commit()

            return food_to_update
        else:
            return None  
        
    async def delete_food_item(self, food_id: str, session: AsyncSession):
        food_to_delete = await self.get_food_by_id(food_id, session)

        if food_to_delete is not None:
            await session.delete(food_to_delete)
            await session.commit()

            return {}
        else:
            return None