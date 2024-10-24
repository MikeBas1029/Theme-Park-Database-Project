from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.park_facilities import ParkFacilities
from src.schemas.park_facilities import ParkFacilitiesCreateModel, ParkFacilitiesUpdateModel, FacilityStatus


class ParkFacilitiesService:
    async def get_all_park_facilities(self, session: AsyncSession):
        query = select(ParkFacilities).order_by(ParkFacilities.facility_name)

        result = await session.exec(query)

        return result.all()
    
    async def get_park_facility_by_id(self, park_facility_id: str, session: AsyncSession):
        query = select(ParkFacilities).where(ParkFacilities.facility_id == park_facility_id)

        result = await session.exec(query)

        park_facility = result.first()

        return park_facility if park_facility is not None else None 
    
    async def park_facility_exists(self, park_facility_id: str, session: AsyncSession):
        query = select(ParkFacilities).where(ParkFacilities.facility_id == park_facility_id)

        result = await session.exec(query)

        park_facility = result.first()

        return bool(park_facility)
    
    async def create_park_facility(
            self,
            park_facility_data: ParkFacilitiesCreateModel,
            session: AsyncSession
    ):
        park_facility_data_dict = park_facility_data.model_dump()

        park_facility_data_dict['status'] = FacilityStatus.ACTIVE.value

        new_park_facility = ParkFacilities(**park_facility_data_dict)

        # First check if park_facility exists already
        existing_park_facility = await self.park_facility_exists(new_park_facility.facility_id, session)

        if existing_park_facility:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"ParkFacilities with park_facility_id {new_park_facility.facility_id} already exists.")
        else:
            session.add(new_park_facility)

            await session.commit()

            return new_park_facility
    

    async def update_park_facility(
            self, 
            park_facility_id: str,
            update_data: ParkFacilitiesUpdateModel,
            session: AsyncSession
    ):
        park_facility_to_update = await self.get_park_facility_by_id(park_facility_id, session)


        if park_facility_to_update is not None:
            park_facility_update_dict = update_data.model_dump()

            for k, v in park_facility_update_dict.items():
                setattr(park_facility_to_update, k, v)

            await session.commit()

            return park_facility_to_update
        else:
            return None  
        
    async def delete_park_facility(self, park_facility_id: str, session: AsyncSession):
        park_facility_to_delete = await self.get_park_facility_by_id(park_facility_id, session)

        if park_facility_to_delete is not None:
            await session.delete(park_facility_to_delete)
            await session.commit()

            return {}
        else:
            return None