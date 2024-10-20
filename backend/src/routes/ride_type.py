from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.ride_type import RideTypeService
from src.schemas.ride_type import RideTypeInputModel, RideTypeOutputModel

ride_type_router = APIRouter()
ride_type_service = RideTypeService()


@ride_type_router.get("/", response_model=List[RideTypeOutputModel])
async def get_all_ride_types(session: AsyncSession = Depends(get_session)):
    ride_types = await ride_type_service.get_all_ride_types(session)
    return ride_types


@ride_type_router.get("/{ride_type_id}", response_model=RideTypeOutputModel) 
async def get_ride_type(ride_type_id: str, session: AsyncSession = Depends(get_session)):
    ride_type = await ride_type_service.get_ride_type_by_id(ride_type_id, session)
    
    if ride_type:
        return ride_type
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"RideType with ride_type_id {ride_type_id} not found.") 



@ride_type_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RideTypeOutputModel,
)
async def create_a_ride_type(
    ride_type_data: RideTypeInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await ride_type_service.create_ride_type(ride_type_data, session)
    except Exception as error:
        raise error



@ride_type_router.patch("/{ride_type_id}", response_model=RideTypeOutputModel)
async def update_ride_type(
    ride_type_id: str,
    update_data: RideTypeInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_ride_type = await ride_type_service.update_ride_type(ride_type_id, update_data, session)

    if updated_ride_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"RideType with ride_type_id {ride_type_id} not found.") 
    else:
        return updated_ride_type


@ride_type_router.delete(
    "/{ride_type_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ride_type(ride_type_id: str, session: AsyncSession = Depends(get_session)):
    ride_type_to_delete = await ride_type_service.delete_ride_type(ride_type_id, session)
    
    if ride_type_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"RideType with ride_type_id {ride_type_id} not found.") 
