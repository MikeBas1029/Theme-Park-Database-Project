from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.work_order_items import WorkOrderItemService
from src.schemas.work_order_items import WorkOrderItemInputModel, WorkOrderItemOutputModel

work_order_item_router = APIRouter()
work_order_item_service = WorkOrderItemService()


@work_order_item_router.get("/", response_model=List[WorkOrderItemOutputModel])
async def get_all_work_order_items(session: AsyncSession = Depends(get_session)):
    work_order_item = await work_order_item_service.get_all_work_order_items(session)
    return work_order_item


@work_order_item_router.get("/{work_order_item_id}", response_model=WorkOrderItemOutputModel) 
async def get_work_order_item(work_order_item_id: str, session: AsyncSession = Depends(get_session)):
    work_order_item = await work_order_item_service.get_work_order_item_by_id(work_order_item_id, session)
    
    if work_order_item:
        return work_order_item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with work_order_item id {work_order_item_id} not found.") 



@work_order_item_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=WorkOrderItemOutputModel,
)
async def create_a_work_order_item(
    work_order_item_data: WorkOrderItemInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await work_order_item_service.create_work_order_item(work_order_item_data, session)
    except Exception as error:
        raise error



@work_order_item_router.patch("/{work_order_item_id}", response_model=WorkOrderItemOutputModel)
async def update_work_order_item(
    work_order_item_id: str,
    update_data: WorkOrderItemInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_work_order_item = await work_order_item_service.update_work_order_item(work_order_item_id, update_data, session)

    if updated_work_order_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with work_order_item id {work_order_item_id} not found.") 
    else:
        return updated_work_order_item


@work_order_item_router.delete(
    "/{work_order_item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_work_order_item(work_order_item_id: str, session: AsyncSession = Depends(get_session)):
    work_order_item_to_delete = await work_order_item_service.delete_work_order_item(work_order_item_id, session)
    
    if work_order_item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with work_order_item id {work_order_item_id} not found.") 
