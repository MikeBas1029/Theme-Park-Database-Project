from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.vendors import VendorService
from src.schemas.vendors import Vendor, VendorCreateModel, VendorUpdateModel

vendor_router = APIRouter()
vendor_service = VendorService()

@vendor_router.get("/", response_model=List[Vendor])
async def get_all_vendors(session: AsyncSession = Depends(get_session)):
    vendors = await vendor_service.get_all_vendors(session)
    return vendors


@vendor_router.get("/{}", response_model=Vendor)
async def get_vendor(vendor_email: str, session: AsyncSession = Depends(get_session)):
    vendor = await vendor_service.get_vendor_by_email(vendor_email, session)

    if vendor:
        return vendor
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor with email {vendor_email} not found.")



@vendor_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Vendor,
)
async def create_a_vendor(
        vendor_data: VendorCreateModel,
        session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await vendor_service.create_vendor(vendor_data, session)
    except Exception as error:
        raise error



@vendor_router.patch("/{vendor_email}", response_model=Vendor)
async def update_vendor(
        vendor_email: str,
        update_data: VendorUpdateModel,
        session: AsyncSession = Depends(get_session),
) -> dict:
    updated_vendor = await vendor_service.update_vendor(vendor_email, update_data, session)

    if updated_vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor with email {vendor_email} not found.")
    else:
        return updated_vendor


@vendor_router.delete(
    "/{vendor_email}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_vendor(vendor_email: str, session: AsyncSession = Depends(get_session)):
    vendor_to_delete = await vendor_service.delete_vendor(vendor_email, session)

    if vendor_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor with email {vendor_email} not found.")
