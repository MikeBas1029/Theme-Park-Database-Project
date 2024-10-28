from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.beverage_items import BeverageItems
from src.schemas.beverage_items import BeverageCreateModel, BeverageUpdateModel

class BeverageService:
    async def get_all_beverages(self, session: AsyncSession):
        query = select(BeverageItems).order_by(BeverageItems.beverage_item)

        result = await session.exec(query)

        return result.all()
    
    async def get_beverage_by_bev_id(self, bev_id: int, session: AsyncSession):
        query = select(BeverageItems).where(BeverageItems.bev_id == bev_id)

        result = await session.exec(query)

        beverage = result.first()

        return beverage if beverage is not None else None 
    
    async def beverage_exists(self, bev_id: int, session: AsyncSession):
        query = select(BeverageItems).where(BeverageItems.bev_id == bev_id)

        result = await session.exec(query)

        beverage = result.first()

        return bool(beverage)
    
    async def create_beverage(
            self,
            bev_id_data: BeverageCreateModel,
            session: AsyncSession
    ):
        bev_id_data_dict = bev_id_data.model_dump()


        new_bev = BeverageItems(**bev_id_data_dict)

        # First check if beverage exists already
        existing_beverage = await self.beverage_exists(new_bev.bev_id, session)

        if existing_beverage:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"BeverageItems with bev_id {new_bev.bev_id} already exists.")
        else:
            session.add(new_bev)

            await session.commit()

            return new_bev
    

    async def update_bev(
            self, 
            bev_id: int,
            update_data: BeverageUpdateModel,
            session: AsyncSession
    ):
        bev_to_update = await self.get_beverage_by_bev_id(bev_id, session)


        if bev_to_update is not None:
            bev_to_update_dict = update_data.model_dump()

            for k, v in bev_to_update_dict.items():
                setattr(bev_to_update, k, v)

            await session.commit()

            return bev_to_update
        else:
            return None  
        
    async def delete_bev_id(self, bev_id: int, session: AsyncSession):
        bev_id_to_delete = await self.get_beverage_by_bev_id(bev_id, session)

        if bev_id_to_delete is not None:
            await session.delete(bev_id_to_delete)
            await session.commit()

            return {}
        else:
            return None