from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.po_details import PurchaseOrderDetailsService
from src.schemas.po_details import PurchaseOrderDetailsInputModel, PurchaseOrderDetailsOutputModel

po_detail_router = APIRouter()
po_detail_service = PurchaseOrderDetailsService()


@po_detail_router.get("/", response_model=List[PurchaseOrderDetailsOutputModel])
async def get_all_po_details(session: AsyncSession = Depends(get_session)):
    po_details = await po_detail_service.get_all_po_details(session)
    return po_details


@po_detail_router.get("/{po_detail_id}", response_model=PurchaseOrderDetailsOutputModel) 
async def get_po_detail(po_detail_id: str, session: AsyncSession = Depends(get_session)):
    po_detail = await po_detail_service.get_po_detail_by_id(po_detail_id, session)
    
    if po_detail:
        return po_detail
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {po_detail_id} not found.") 



@po_detail_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseOrderDetailsOutputModel,
)
async def create_a_po_detail(
    po_detail_data: PurchaseOrderDetailsInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await po_detail_service.create_po_detail(po_detail_data, session)
    except Exception as error:
        raise error



@po_detail_router.patch("/{po_detail_id}", response_model=PurchaseOrderDetailsOutputModel)
async def update_po_detail(
    po_detail_id: str,
    update_data: PurchaseOrderDetailsInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_po_detail = await po_detail_service.update_po_detail(po_detail_id, update_data, session)

    if updated_po_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {po_detail_id} not found.") 
    else:
        return updated_po_detail


@po_detail_router.delete(
    "/{po_detail_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_po_detail(po_detail_id: str, session: AsyncSession = Depends(get_session)):
    po_detail_to_delete = await po_detail_service.delete_po_detail(po_detail_id, session)
    
    if po_detail_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {po_detail_id} not found.") 
