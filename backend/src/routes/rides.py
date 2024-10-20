from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.rides import RideService
from src.schemas.rides import Ride, RideCreateModel, RideUpdateModel

ride_router = APIRouter()
ride_service = RideService()


@ride_router.get("/", response_model=List[Ride])
async def get_all_rides(session: AsyncSession = Depends(get_session)):
    rides = await ride_service.get_all_rides(session)
    return rides


@ride_router.get("/{ride_id}", response_model=Ride) 
async def get_ride(ride_id: str, session: AsyncSession = Depends(get_session)):
    ride = await ride_service.get_ride_by_id(ride_id, session)
    
    if ride:
        return ride
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ride with ride_id {ride_id} not found.") 



@ride_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Ride,
)
async def create_a_ride(
    ride_data: RideCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await ride_service.create_ride(ride_data, session)
    except Exception as error:
        raise error



@ride_router.patch("/{ride_id}", response_model=Ride)
async def update_ride(
    ride_id: str,
    update_data: RideUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_ride = await ride_service.update_ride(ride_id, update_data, session)

    if updated_ride is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ride with ride_id {ride_id} not found.") 
    else:
        return updated_ride


@ride_router.delete(
    "/{ride_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ride(ride_id: str, session: AsyncSession = Depends(get_session)):
    ride_to_delete = await ride_service.delete_ride(ride_id, session)
    
    if ride_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ride with ride_id {ride_id} not found.") 
