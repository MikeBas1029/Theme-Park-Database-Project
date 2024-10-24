from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.park_facilities import ParkFacilitiesService
from src.schemas.park_facilities import ParkFacilities, ParkFacilitiesCreateModel, ParkFacilitiesUpdateModel

park_facilities_router = APIRouter()
park_facilities_service = ParkFacilitiesService()


@park_facilities_router.get("/", response_model=List[ParkFacilities])
async def get_all_park_facilities(session: AsyncSession = Depends(get_session)):
    park_facilities = await park_facilities_service.get_all_park_facilities(session)
    return park_facilities


@park_facilities_router.get("/{park_facility_id}", response_model=ParkFacilities) 
async def get_park_facility(park_facility_id: str, session: AsyncSession = Depends(get_session)):
    park_facility = await park_facilities_service.get_park_facility_by_id(park_facility_id, session)
    
    if park_facility:
        return park_facility
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ParkFacilities with park_facilities id {park_facility_id} not found.") 



@park_facilities_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ParkFacilities,
)
async def create_a_park_facility(
    park_facility_data: ParkFacilitiesCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await park_facilities_service.create_park_facility(park_facility_data, session)
    except Exception as error:
        raise error



@park_facilities_router.patch("/{park_facility_id}", response_model=ParkFacilities)
async def update_park_facility(
    park_facility_id: str,
    update_data: ParkFacilitiesUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_park_facility = await park_facilities_service.update_park_facility(park_facility_id, update_data, session)

    if updated_park_facility is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ParkFacilities with park_facility id {park_facility_id} not found.") 
    else:
        return updated_park_facility


@park_facilities_router.delete(
    "/{park_facility_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_park_facility(park_facility_id: str, session: AsyncSession = Depends(get_session)):
    park_facilities_to_delete = await park_facilities_service.delete_park_facility(park_facility_id, session)
    
    if park_facilities_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ParkFacilities with park_facilities id {park_facility_id} not found.") 
