from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.purchase_orders import PurchaseOrderService
from src.schemas.purchase_orders import PurchaseOrder, PurchaseOrderCreateModel, PurchaseOrderUpdateModel

purchase_order_router = APIRouter()
purchase_order_service = PurchaseOrderService()


@purchase_order_router.get("/", response_model=List[PurchaseOrder])
async def get_all_purchase_orders(session: AsyncSession = Depends(get_session)):
    purchase_orders = await purchase_order_service.get_all_purchase_orders(session)
    return purchase_orders


@purchase_order_router.get("/{purchase_order_id}", response_model=PurchaseOrder) 
async def get_purchase_order(purchase_order_id: str, session: AsyncSession = Depends(get_session)):
    purchase_order = await purchase_order_service.get_purchase_order_by_id(purchase_order_id, session)
    
    if purchase_order:
        return purchase_order
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {purchase_order_id} not found.") 



@purchase_order_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PurchaseOrder,
)
async def create_a_purchase_order(
    purchase_order_data: PurchaseOrderCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await purchase_order_service.create_purchase_order(purchase_order_data, session)
    except Exception as error:
        raise error



@purchase_order_router.patch("/{purchase_order_id}", response_model=PurchaseOrder)
async def update_purchase_order(
    purchase_order_id: str,
    update_data: PurchaseOrderUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_purchase_order = await purchase_order_service.update_purchase_order(purchase_order_id, update_data, session)

    if updated_purchase_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {purchase_order_id} not found.") 
    else:
        return updated_purchase_order


@purchase_order_router.delete(
    "/{purchase_order_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_purchase_order(purchase_order_id: str, session: AsyncSession = Depends(get_session)):
    purchase_order_to_delete = await purchase_order_service.delete_purchase_order(purchase_order_id, session)
    
    if purchase_order_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Purchase Order with ID {purchase_order_id} not found.") 
