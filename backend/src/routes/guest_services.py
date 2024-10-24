from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.guest_services import GuestServicesService
from src.schemas.guest_services import GuestServiceInputModel, GuestServiceOutputModel

guest_services_router = APIRouter()
guest_services_service = GuestServicesService()


@guest_services_router.get("/", response_model=List[GuestServiceOutputModel])
async def get_all_guest_services(session: AsyncSession = Depends(get_session)):
    guest_services = await guest_services_service.get_all_guest_services(session)
    return guest_services


@guest_services_router.get("/{guest_services_id}", response_model=GuestServiceOutputModel) 
async def get_guest_services(guest_services_id: str, session: AsyncSession = Depends(get_session)):
    guest_services = await guest_services_service.get_guest_service_by_id(guest_services_id, session)
    
    if guest_services:
        return guest_services
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"GuestServices with guest_services {guest_services_id} not found.") 



@guest_services_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=GuestServiceOutputModel,
)
async def create_a_guest_service(
    guest_services_data: GuestServiceInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await guest_services_service.create_guest_service(guest_services_data, session)
    except Exception as error:
        raise error



@guest_services_router.patch("/{guest_services_id}", response_model=GuestServiceOutputModel)
async def update_guest_service(
    guest_services_id: str,
    update_data: GuestServiceInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_guest_services = await guest_services_service.update_guest_service(guest_services_id, update_data, session)

    if updated_guest_services is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"GuestServices with guest_services {guest_services_id} not found.") 
    else:
        return updated_guest_services


@guest_services_router.delete(
    "/{guest_services_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_guest_service(guest_services_id: str, session: AsyncSession = Depends(get_session)):
    guest_services_to_delete = await guest_services_service.delete_guest_service(guest_services_id, session)
    
    if guest_services_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"GuestServices with guest_services {guest_services_id} not found.") 
