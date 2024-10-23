from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.vendors import Vendors
from src.schemas.vendors import VendorCreateModel, VendorUpdateModel

class VendorService:
    async def get_all_vendors(self, session: AsyncSession):
        query = select(Vendors).order_by(Vendors.vendor_id)

        result = await session.exec(query)

        return result.all()

    async def get_vendor_by_email(self, vendor_email: str, session: AsyncSession):
        query = select(Vendors).where(Vendors.email == vendor_email)

        result = await session.exec(query)

        vendor = result.first()

        return vendor if vendor is not None else None

    async def vendor_exists(self, vendor_email: str, session: AsyncSession):
        query = select(Vendors).where(Vendors.email == vendor_email)

        result = await session.exec(query)

        vendor = result.first()

        return bool(vendor)

    async def create_vendor(
            self,
            vendor_data: VendorCreateModel,
            session: AsyncSession
    ):
        vendor_data_dict = vendor_data.model_dump()

        new_vendor = Vendors(**vendor_data_dict)

        # First check if vendor exists already
        existing_vendor = await self.vendor_exists(new_vendor.email, session)

        if existing_vendor:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vendor with email {new_vendor.email} already exists.")
        else:
            session.add(new_vendor)

            await session.commit()

            return new_vendor


    async def update_vendor(
            self,
            vendor_email: str,
            update_data: VendorUpdateModel,
            session: AsyncSession
    ):
        vendor_to_update = await self.get_vendor_by_email(vendor_email, session)


        if vendor_to_update is not None:
            vendor_update_dict = update_data.model_dump()

            for k, v in vendor_update_dict.items():
                setattr(vendor_to_update, k, v)

            await session.commit()

            return vendor_to_update
        else:
            return None

    async def delete_vendor(self, vendor_email: str, session: AsyncSession):
        vendor_to_delete = await self.get_vendor_by_email(vendor_email, session)

        if vendor_to_delete is not None:
            await session.delete(vendor_to_delete)
            await session.commit()

            return {}
        else:
            return None