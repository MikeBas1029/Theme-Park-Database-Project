from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.ride_type import RideType 
from src.schemas.ride_type import RideTypeInputModel

class RideTypeService:
    async def get_all_ride_types(self, session: AsyncSession):
        query = select(RideType).order_by(RideType.ride_type)

        result = await session.exec(query)

        return result.all()
    
    async def get_ride_type_by_id(self, ride_type_id: str, session: AsyncSession):
        query = select(RideType).where(RideType.ride_type_id == ride_type_id)

        result = await session.exec(query)

        ride_type = result.first()

        return ride_type if ride_type is not None else None 
    
    async def ride_type_exists(self, ride_type_id: str, session: AsyncSession):
        query = select(RideType).where(RideType.ride_type_id == ride_type_id)

        result = await session.exec(query)

        ride_type = result.first()

        return bool(ride_type)
    
    async def create_ride_type(
            self,
            ride_type_data: RideTypeInputModel,
            session: AsyncSession
    ):
        ride_type_data_dict = ride_type_data.model_dump()

        new_ride_type = RideType(**ride_type_data_dict)

        # First check if ride_type exists already
        existing_ride_type = await self.ride_type_exists(new_ride_type.ride_type_id, session)

        if existing_ride_type:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ride with ride_type_id {new_ride_type.ride_type_id} already exists.")
        else:
            session.add(new_ride_type)

            await session.commit()

            return new_ride_type
    

    async def update_ride_type(
            self, 
            ride_type_id: str,
            update_data: RideTypeInputModel,
            session: AsyncSession
    ):
        ride_type_to_update = await self.get_ride_type_by_id(ride_type_id, session)


        if ride_type_to_update is not None:
            ride_type_update_dict = update_data.model_dump()

            for k, v in ride_type_update_dict.items():
                setattr(ride_type_to_update, k, v)

            await session.commit()

            return ride_type_to_update
        else:
            return None  
        
    async def delete_ride_type(self, ride_type_id: str, session: AsyncSession):
        ride_type_to_delete = await self.get_ride_type_by_id(ride_type_id, session)

        if ride_type_to_delete is not None:
            await session.delete(ride_type_to_delete)
            await session.commit()

            return {}
        else:
            return None