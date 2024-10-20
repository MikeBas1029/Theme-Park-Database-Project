from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.ride_usage import RideUsage 
from src.schemas.ride_usage import RideUsageInputModel

class RideUsageService:
    async def get_all_ride_usages(self, session: AsyncSession):
        query = select(RideUsage).order_by(RideUsage.usage_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_ride_usage_by_id(self, ride_usage_id: str, session: AsyncSession):
        query = select(RideUsage).where(RideUsage.ride_usage_id == ride_usage_id)

        result = await session.exec(query)

        ride_usage = result.first()

        return ride_usage if ride_usage is not None else None 
    
    async def ride_usage_exists(self, ride_usage_id: str, session: AsyncSession):
        query = select(RideUsage).where(RideUsage.ride_usage_id == ride_usage_id)

        result = await session.exec(query)

        ride_usage = result.first()

        return bool(ride_usage)
    
    async def create_ride_usage(
            self,
            ride_usage_data: RideUsageInputModel,
            session: AsyncSession
    ):
        ride_usage_data_dict = ride_usage_data.model_dump()

        new_ride_usage = RideUsage(**ride_usage_data_dict)

        # First check if ride_usage exists already
        existing_ride_usage = await self.ride_usage_exists(new_ride_usage.ride_usage_id, session)

        if existing_ride_usage:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Record with ride_usage_id {new_ride_usage.ride_usage_id} already exists.")
        else:
            session.add(new_ride_usage)

            await session.commit()

            return new_ride_usage
    

    async def update_ride_usage(
            self, 
            ride_usage_id: str,
            update_data: RideUsageInputModel,
            session: AsyncSession
    ):
        ride_usage_to_update = await self.get_ride_usage_by_id(ride_usage_id, session)


        if ride_usage_to_update is not None:
            ride_usage_update_dict = update_data.model_dump()

            for k, v in ride_usage_update_dict.items():
                setattr(ride_usage_to_update, k, v)

            await session.commit()

            return ride_usage_to_update
        else:
            return None  
        
    async def delete_ride_usage(self, ride_usage_id: str, session: AsyncSession):
        ride_usage_to_delete = await self.get_ride_usage_by_id(ride_usage_id, session)

        if ride_usage_to_delete is not None:
            await session.delete(ride_usage_to_delete)
            await session.commit()

            return {}
        else:
            return None