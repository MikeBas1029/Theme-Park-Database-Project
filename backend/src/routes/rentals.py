from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.rentals import RentalsService
from src.schemas.rentals import RentalsInputModel, RentalsOutputModel

rental_router = APIRouter()
rental_service = RentalsService()


@rental_router.get("/", response_model=List[RentalsOutputModel])
async def get_all_rentals(session: AsyncSession = Depends(get_session)):
    rental = await rental_service.get_all_rentals(session)
    return rental


@rental_router.get("/{rental_id}", response_model=RentalsOutputModel) 
async def get_rental(rental_id: str, session: AsyncSession = Depends(get_session)):
    rental = await rental_service.get_rental_by_id(rental_id, session)
    
    if rental:
        return rental
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rentals with rental id {rental_id} not found.") 



@rental_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RentalsOutputModel,
)
async def create_a_rental(
    rental_data: RentalsInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await rental_service.create_rental(rental_data, session)
    except Exception as error:
        raise error



@rental_router.patch("/{rental_id}", response_model=RentalsOutputModel)
async def update_rental(
    rental_id: str,
    update_data: RentalsInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_rental = await rental_service.update_rental(rental_id, update_data, session)

    if updated_rental is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rentals with rental id {rental_id} not found.") 
    else:
        return updated_rental


@rental_router.delete(
    "/{rental_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_rental(rental_id: str, session: AsyncSession = Depends(get_session)):
    rental_to_delete = await rental_service.delete_rental(rental_id, session)
    
    if rental_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rentals with rental id {rental_id} not found.") 
