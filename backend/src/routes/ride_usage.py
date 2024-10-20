from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.ride_usage import RideUsageService
from src.schemas.ride_usage import RideUsageInputModel, RideUsageOutputModel

ride_usage_router = APIRouter()
ride_usage_service = RideUsageService()


@ride_usage_router.get("/", response_model=List[RideUsageOutputModel])
async def get_all_ride_usages(session: AsyncSession = Depends(get_session)):
    ride_usages = await ride_usage_service.get_all_ride_usages(session)
    return ride_usages


@ride_usage_router.get("/{ride_usage_id}", response_model=RideUsageOutputModel) 
async def get_ride_usage(ride_usage_id: str, session: AsyncSession = Depends(get_session)):
    ride_usage = await ride_usage_service.get_ride_usage_by_id(ride_usage_id, session)
    
    if ride_usage:
        return ride_usage
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ride_usage_id {ride_usage_id} not found.") 



@ride_usage_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RideUsageOutputModel,
)
async def create_a_ride_usage(
    ride_usage_data: RideUsageInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await ride_usage_service.create_ride_usage(ride_usage_data, session)
    except Exception as error:
        raise error



@ride_usage_router.patch("/{ride_usage_id}", response_model=RideUsageOutputModel)
async def update_ride_usage(
    ride_usage_id: str,
    update_data: RideUsageInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_ride_usage = await ride_usage_service.update_ride_usage(ride_usage_id, update_data, session)

    if updated_ride_usage is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ride_usage_id {ride_usage_id} not found.") 
    else:
        return updated_ride_usage


@ride_usage_router.delete(
    "/{ride_usage_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ride_usage(ride_usage_id: str, session: AsyncSession = Depends(get_session)):
    ride_usage_to_delete = await ride_usage_service.delete_ride_usage(ride_usage_id, session)
    
    if ride_usage_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ride_usage_id {ride_usage_id} not found.") 
