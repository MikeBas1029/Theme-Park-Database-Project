from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.purchase_order_items import PurchaseOrderItemService
from src.schemas.purchase_order_items import PurchaseOrderItemInputModel, PurchaseOrderItemOutputModel

purchase_order_item_router = APIRouter()
purchase_order_item_service = PurchaseOrderItemService()


@purchase_order_item_router.get("/", response_model=List[PurchaseOrderItemOutputModel])
async def get_all_purchase_order_items(session: AsyncSession = Depends(get_session)):
    purchase_order_items = await purchase_order_item_service.get_all_purchase_order_items(session)
    return purchase_order_items


@purchase_order_item_router.get("/{purchase_order_item_id}", response_model=PurchaseOrderItemOutputModel) 
async def get_purchase_order_item(purchase_order_item_id: str, session: AsyncSession = Depends(get_session)):
    purchase_order_item = await purchase_order_item_service.get_purchase_order_item_by_id(purchase_order_item_id, session)
    
    if purchase_order_item:
        return purchase_order_item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {purchase_order_item_id} not found.") 



@purchase_order_item_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseOrderItemOutputModel,
)
async def create_a_purchase_order_item(
    purchase_order_item_data: PurchaseOrderItemInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await purchase_order_item_service.create_purchase_order_item(purchase_order_item_data, session)
    except Exception as error:
        raise error



@purchase_order_item_router.patch("/{purchase_order_item_id}", response_model=PurchaseOrderItemOutputModel)
async def update_purchase_order_item(
    purchase_order_item_id: str,
    update_data: PurchaseOrderItemInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_purchase_order_item = await purchase_order_item_service.update_purchase_order_item(purchase_order_item_id, update_data, session)

    if updated_purchase_order_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {purchase_order_item_id} not found.") 
    else:
        return updated_purchase_order_item


@purchase_order_item_router.delete(
    "/{purchase_order_item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_purchase_order_item(purchase_order_item_id: str, session: AsyncSession = Depends(get_session)):
    purchase_order_item_to_delete = await purchase_order_item_service.delete_purchase_order_item(purchase_order_item_id, session)
    
    if purchase_order_item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {purchase_order_item_id} not found.") 
