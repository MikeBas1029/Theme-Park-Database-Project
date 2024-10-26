from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.work_orders import WorkOrderService
from src.schemas.work_orders import WorkOrderOutputModel, WorkOrderCreateModel, WorkOrderUpdateModel

work_order_router = APIRouter()
work_order_service = WorkOrderService()


@work_order_router.get("/", response_model=List[WorkOrderOutputModel])
async def get_all_work_orders(session: AsyncSession = Depends(get_session)):
    work_orders = await work_order_service.get_all_work_orders(session)
    return work_orders


@work_order_router.get("/{work_order_id}", response_model=WorkOrderOutputModel) 
async def get_work_order(work_order_id: str, session: AsyncSession = Depends(get_session)):
    work_order = await work_order_service.get_work_order_by_id(work_order_id, session)
    
    if work_order:
        return work_order
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"WorkOrder with work_order_id {work_order_id} not found.") 



@work_order_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=WorkOrderOutputModel,
)
async def create_a_work_order(
    work_order_data: WorkOrderCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await work_order_service.create_work_order(work_order_data, session)
    except Exception as error:
        raise error



@work_order_router.patch("/{work_order_id}", response_model=WorkOrderOutputModel)
async def update_work_order(
    work_order_id: str,
    update_data: WorkOrderUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_work_order = await work_order_service.update_work_order(work_order_id, update_data, session)

    if updated_work_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"WorkOrder with work_order_id {work_order_id} not found.") 
    else:
        return updated_work_order


@work_order_router.delete(
    "/{work_order_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_work_order(work_order_id: str, session: AsyncSession = Depends(get_session)):
    work_order_to_delete = await work_order_service.delete_work_order(work_order_id, session)
    
    if work_order_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"WorkOrder with work_order_id {work_order_id} not found.") 
