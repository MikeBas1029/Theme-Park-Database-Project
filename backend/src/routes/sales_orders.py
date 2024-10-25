from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.sales_orders import SalesOrdersService
from src.schemas.sales_orders import SalesOrdersInputModel, SalesOrdersOutputModel

sales_order_router = APIRouter()
sales_order_service = SalesOrdersService()


@sales_order_router.get("/", response_model=List[SalesOrdersOutputModel])
async def get_all_sales_orders(session: AsyncSession = Depends(get_session)):
    sales_order = await sales_order_service.get_all_sales_orders(session)
    return sales_order


@sales_order_router.get("/{sales_order_id}", response_model=SalesOrdersOutputModel) 
async def get_sales_order(sales_order_id: str, session: AsyncSession = Depends(get_session)):
    sales_order = await sales_order_service.get_show_by_id(sales_order_id, session)
    
    if sales_order:
        return sales_order
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales order with transaction ID {sales_order_id} not found.") 



@sales_order_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SalesOrdersOutputModel,
)
async def create_a_sales_order(
    sales_order_data: SalesOrdersInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await sales_order_service.create_show(sales_order_data, session)
    except Exception as error:
        raise error



@sales_order_router.patch("/{sales_order_id}", response_model=SalesOrdersOutputModel)
async def update_sales_order(
    sales_order_id: str,
    update_data: SalesOrdersInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_sales_order = await sales_order_service.update_show(sales_order_id, update_data, session)

    if updated_sales_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales order with transaction ID {sales_order_id} not found.") 
    else:
        return updated_sales_order


@sales_order_router.delete(
    "/{sales_order_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_sales_order(sales_order_id: str, session: AsyncSession = Depends(get_session)):
    sales_order_to_delete = await sales_order_service.delete_show(sales_order_id, session)
    
    if sales_order_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales order with transaction ID {sales_order_id} not found.") 
