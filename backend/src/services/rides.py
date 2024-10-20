from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.rides import Rides 
from src.schemas.rides import RideCreateModel, RideUpdateModel

class RideService:
    async def get_all_rides(self, session: AsyncSession):
        query = select(Rides).order_by(Rides.name)

        result = await session.exec(query)

        return result.all()
    
    async def get_ride_by_id(self, ride_id: str, session: AsyncSession):
        query = select(Rides).where(Rides.ride_id == ride_id)

        result = await session.exec(query)

        ride = result.first()

        return ride if ride is not None else None 
    
    async def ride_exists(self, ride_id: str, session: AsyncSession):
        query = select(Rides).where(Rides.ride_id == ride_id)

        result = await session.exec(query)

        ride = result.first()

        return bool(ride)
    
    async def create_ride(
            self,
            ride_data: RideCreateModel,
            session: AsyncSession
    ):
        ride_data_dict = ride_data.model_dump()

        new_ride = Rides(**ride_data_dict)

        # First check if ride exists already
        existing_ride = await self.ride_exists(new_ride.ride_id, session)

        if existing_ride:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ride with ride_id {new_ride.ride_id} already exists.")
        else:
            session.add(new_ride)

            await session.commit()

            return new_ride
    

    async def update_ride(
            self, 
            ride_id: str,
            update_data: RideUpdateModel,
            session: AsyncSession
    ):
        ride_to_update = await self.get_ride_by_id(ride_id, session)


        if ride_to_update is not None:
            ride_update_dict = update_data.model_dump()

            for k, v in ride_update_dict.items():
                setattr(ride_to_update, k, v)

            await session.commit()

            return ride_to_update
        else:
            return None  
        
    async def delete_ride(self, ride_id: str, session: AsyncSession):
        ride_to_delete = await self.get_ride_by_id(ride_id, session)

        if ride_to_delete is not None:
            await session.delete(ride_to_delete)
            await session.commit()

            return {}
        else:
            return None