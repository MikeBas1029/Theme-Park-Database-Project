from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.sales_order_details import SalesOrderDetailService
from src.schemas.sales_order_details import SalesOrderDetailInputModel, SalesOrderDetailOutputModel

sales_order_detail_router = APIRouter()
sales_order_detail_service = SalesOrderDetailService()


@sales_order_detail_router.get("/", response_model=List[SalesOrderDetailOutputModel])
async def get_all_sales_order_details(session: AsyncSession = Depends(get_session)):
    sales_order_detail = await sales_order_detail_service.get_all_sales_order_details(session)
    return sales_order_detail


@sales_order_detail_router.get("/{sales_order_detail_id}", response_model=SalesOrderDetailOutputModel) 
async def get_sales_order_detail(sales_order_detail_id: str, session: AsyncSession = Depends(get_session)):
    sales_order_detail = await sales_order_detail_service.get_so_detail_by_id(sales_order_detail_id, session)
    
    if sales_order_detail:
        return sales_order_detail
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales order with sales order detail ID {sales_order_detail_id} not found.") 



@sales_order_detail_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SalesOrderDetailOutputModel,
)
async def create_a_sales_order_detail(
    sales_order_detail_data: SalesOrderDetailInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await sales_order_detail_service.create_so_detail(sales_order_detail_data, session)
    except Exception as error:
        raise error



@sales_order_detail_router.patch("/{sales_order_detail_id}", response_model=SalesOrderDetailOutputModel)
async def update_sales_order_detail(
    sales_order_detail_id: str,
    update_data: SalesOrderDetailInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_sales_order_detail = await sales_order_detail_service.update_so_detail(sales_order_detail_id, update_data, session)

    if updated_sales_order_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales order with sales order detail ID {sales_order_detail_id} not found.") 
    else:
        return updated_sales_order_detail


@sales_order_detail_router.delete(
    "/{sales_order_detail_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_sales_order_detail(sales_order_detail_id: str, session: AsyncSession = Depends(get_session)):
    sales_order_detail_to_delete = await sales_order_detail_service.delete_so_detail(sales_order_detail_id, session)
    
    if sales_order_detail_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales order with sales order detail ID {sales_order_detail_id} not found.") 
