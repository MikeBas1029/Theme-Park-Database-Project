from typing import List 
from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.supplies import SuppliesService
from src.schemas.supplies import Supplies, SuppliesCreateModel, SuppliesUpdateModel
from src.security import AccessTokenBearer

supplies_router = APIRouter()
supplies_service = SuppliesService()


@supplies_router.get("/", response_model=List[Supplies])
async def get_all_supplies(
    session: AsyncSession = Depends(get_session), 
):
    supplies = await supplies_service.get_all_supplies(session)
    return supplies


@supplies_router.get("/{supply_id}", response_model=Supplies) 
async def get_a_supply(
    supply_id: str, 
    session: AsyncSession = Depends(get_session),
):
    supplies = await supplies_service.get_supply_by_id(supply_id, session)
    
    if supplies:
        return supplies
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplies with id {supply_id} not found.") 



@supplies_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Supplies,
)
async def create_a_supply(
    supply_data: SuppliesCreateModel,
    session: AsyncSession = Depends(get_session),

) -> dict:
    try:
        return await supplies_service.create_supply(supply_data, session)
    except Exception as error:
        raise error



@supplies_router.patch("/{supply_id}", response_model=Supplies)
async def update_supply(
    supply_id: str,
    update_data: SuppliesUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_supplies = await supplies_service.update_supply(supply_id, update_data, session)

    if updated_supplies is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplies with id {supply_id} not found.") 
    else:
        return updated_supplies


@supplies_router.delete(
    "/{supply_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_supplies(
    supply_id: str, 
    session: AsyncSession = Depends(get_session), 
):
    supplies_to_delete = await supplies_service.delete_supply(supply_id, session)
    
    if supplies_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supplies with id {supply_id} not found.") 
