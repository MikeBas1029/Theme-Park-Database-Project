from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.vendor_payments import VendorPaymentService
from src.schemas.vendor_payments import VendorPaymentInputModel, VendorPaymentOutputModel

vendor_payment_router = APIRouter()
vendor_payment_service = VendorPaymentService()


@vendor_payment_router.get("/", response_model=List[VendorPaymentOutputModel])
async def get_all_vendor_payments(session: AsyncSession = Depends(get_session)):
    vendor_payment = await vendor_payment_service.get_all_vendor_payments(session)
    return vendor_payment


@vendor_payment_router.get("/{vendor_payment_id}", response_model=VendorPaymentOutputModel) 
async def get_vendor_payment(vendor_payment_id: str, session: AsyncSession = Depends(get_session)):
    vendor_payment = await vendor_payment_service.get_vendor_payment_by_id(vendor_payment_id, session)
    
    if vendor_payment:
        return vendor_payment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with vendor_payment id {vendor_payment_id} not found.") 



@vendor_payment_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=VendorPaymentOutputModel,
)
async def create_a_vendor_payment(
    vendor_payment_data: VendorPaymentInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await vendor_payment_service.create_vendor_payment(vendor_payment_data, session)
    except Exception as error:
        raise error



@vendor_payment_router.patch("/{vendor_payment_id}", response_model=VendorPaymentOutputModel)
async def update_vendor_payment(
    vendor_payment_id: str,
    update_data: VendorPaymentInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_vendor_payment = await vendor_payment_service.update_vendor_payment(vendor_payment_id, update_data, session)

    if updated_vendor_payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with vendor_payment id {vendor_payment_id} not found.") 
    else:
        return updated_vendor_payment


@vendor_payment_router.delete(
    "/{vendor_payment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_vendor_payment(vendor_payment_id: str, session: AsyncSession = Depends(get_session)):
    vendor_payment_to_delete = await vendor_payment_service.delete_vendor_payment(vendor_payment_id, session)
    
    if vendor_payment_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with vendor_payment id {vendor_payment_id} not found.") 
