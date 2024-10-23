from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.supplies import Supplies 
from src.schemas.supplies import SuppliesCreateModel, SuppliesUpdateModel

class SuppliesService:
    async def get_all_supplies(self, session: AsyncSession):
        query = select(Supplies).order_by(Supplies.name)

        result = await session.exec(query)

        return result.all()
    
    async def get_supply_by_id(self, supply_id: str, session: AsyncSession):
        query = select(Supplies).where(Supplies.supply_id == supply_id)

        result = await session.exec(query)

        supply = result.first()

        return supply if supply is not None else None 
    
    async def supply_exists(self, supply_id: str, session: AsyncSession):
        query = select(Supplies).where(Supplies.supply_id == supply_id)

        result = await session.exec(query)

        supply = result.first()

        return bool(supply)
    
    async def create_supply(
            self,
            supply_data: SuppliesCreateModel,
            session: AsyncSession
    ):
        supply_data_dict = supply_data.model_dump()

        supply_data_dict['on_hand_amount'] = 0

        new_supply = Supplies(**supply_data_dict)

        # First check if supply exists already
        existing_supply = await self.supply_exists(new_supply.supply_id, session)

        if existing_supply:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Supplies with supply_id {new_supply.supply_id} already exists.")
        else:
            session.add(new_supply)

            await session.commit()

            return new_supply
    

    async def update_supply(
            self, 
            supply_id: str,
            update_data: SuppliesUpdateModel,
            session: AsyncSession
    ):
        supply_to_update = await self.get_supply_by_id(supply_id, session)


        if supply_to_update is not None:
            supply_update_dict = update_data.model_dump()

            for k, v in supply_update_dict.items():
                setattr(supply_to_update, k, v)

            await session.commit()

            return supply_to_update
        else:
            return None  
        
    async def delete_supply(self, supply_id: str, session: AsyncSession):
        supply_to_delete = await self.get_supply_by_id(supply_id, session)

        if supply_to_delete is not None:
            await session.delete(supply_to_delete)
            await session.commit()

            return {}
        else:
            return None