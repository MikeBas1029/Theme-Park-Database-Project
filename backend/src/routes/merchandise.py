from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.merchandise import MerchandiseService
from src.schemas.merchandise import MerchandiseInputModel, MerchandiseOutputModel

merchandise_router = APIRouter()
merchandise_service = MerchandiseService()


@merchandise_router.get("/", response_model=List[MerchandiseOutputModel])
async def get_all_merchandise(session: AsyncSession = Depends(get_session)):
    merchandise = await merchandise_service.get_all_merchandise(session)
    return merchandise


@merchandise_router.get("/{merchandise_id}", response_model=MerchandiseOutputModel) 
async def get_merchandise(merchandise_id: str, session: AsyncSession = Depends(get_session)):
    merchandise = await merchandise_service.get_merchandise_by_id(merchandise_id, session)
    
    if merchandise:
        return merchandise
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Merchandise with merchandise id {merchandise_id} not found.") 



@merchandise_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MerchandiseOutputModel,
)
async def create_a_merchandise(
    merchandise_data: MerchandiseInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await merchandise_service.create_merchandise(merchandise_data, session)
    except Exception as error:
        raise error



@merchandise_router.patch("/{merchandise_id}", response_model=MerchandiseOutputModel)
async def update_merchandise(
    merchandise_id: str,
    update_data: MerchandiseInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_merchandise = await merchandise_service.update_merchandise(merchandise_id, update_data, session)

    if updated_merchandise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Merchandise with merchandise id {merchandise_id} not found.") 
    else:
        return updated_merchandise


@merchandise_router.delete(
    "/{merchandise_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_merchandise(merchandise_id: str, session: AsyncSession = Depends(get_session)):
    merchandise_to_delete = await merchandise_service.delete_merchandise(merchandise_id, session)
    
    if merchandise_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Merchandise with merchandise id {merchandise_id} not found.") 
