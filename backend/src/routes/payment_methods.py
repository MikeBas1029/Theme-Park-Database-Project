from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.payment_methods import PaymentMethodService
from src.schemas.payment_methods import PaymentMethodInputModel, PaymentMethodOutputModel

payment_method_router = APIRouter()
payment_method_service = PaymentMethodService()


@payment_method_router.get("/", response_model=List[PaymentMethodOutputModel])
async def get_all_payment_methods(session: AsyncSession = Depends(get_session)):
    payment_methods = await payment_method_service.get_all_payment_methods(session)
    return payment_methods


@payment_method_router.get("/{method_id}", response_model=PaymentMethodOutputModel) 
async def get_payment_method(method_id: int, session: AsyncSession = Depends(get_session)):
    payment_method = await payment_method_service.get_payment_method_by_id(method_id, session)
    
    if payment_method:
        return payment_method
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment method record with method id {method_id} not found.") 



@payment_method_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentMethodOutputModel,
)
async def create_a_payment_method(
    payment_data: PaymentMethodInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await payment_method_service.create_payment_method(payment_data, session)
    except Exception as error:
        raise error



@payment_method_router.patch("/{method_id}", response_model=PaymentMethodOutputModel)
async def update_payment_method(
    method_id: int,
    update_data: PaymentMethodInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_payment_method = await payment_method_service.update_payment(method_id, update_data, session)

    if updated_payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment method record with method id {method_id} not found.") 
    else:
        return updated_payment_method


@payment_method_router.delete(
    "/{method_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_payment_method(method_id: int, session: AsyncSession = Depends(get_session)):
    payment_method_to_delete = await payment_method_service.delete_payment(method_id, session)
    
    if payment_method_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment method record with method id {method_id} not found.") 
