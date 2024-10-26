from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.vendor_payments import VendorPayments
from src.schemas.vendor_payments import VendorPaymentInputModel


class VendorPaymentService:
    async def get_all_vendor_payments(self, session: AsyncSession):
        query = select(VendorPayments).order_by(VendorPayments.payment_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_vendor_payment_by_id(self, vendor_payment_id: str, session: AsyncSession):
        query = select(VendorPayments).where(VendorPayments.vendor_payment_id == vendor_payment_id)

        result = await session.exec(query)

        vendor_payment = result.first()

        return vendor_payment if vendor_payment is not None else None 
    
    async def vendor_payment_exists(self, vendor_payment_id: str, session: AsyncSession):
        query = select(VendorPayments).where(VendorPayments.vendor_payment_id == vendor_payment_id)

        result = await session.exec(query)

        vendor_payment = result.first()

        return bool(vendor_payment)
    
    async def create_vendor_payment(
            self,
            vendor_payment_data: VendorPaymentInputModel,
            session: AsyncSession
    ):
        vendor_payment_data_dict = vendor_payment_data.model_dump()

        new_vendor_payment = VendorPayments(**vendor_payment_data_dict)

        # First check if vendor_payment exists already
        existing_vendor_payment = await self.vendor_payment_exists(new_vendor_payment.vendor_payment_id, session)

        if existing_vendor_payment:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"VendorPayment with vendor_payment_id {new_vendor_payment.vendor_payment_id} already exists.")
        else:
            session.add(new_vendor_payment)

            await session.commit()

            return new_vendor_payment
    

    async def update_vendor_payment(
            self, 
            vendor_payment_id: str,
            update_data: VendorPaymentInputModel,
            session: AsyncSession
    ):
        vendor_payment_to_update = await self.get_vendor_payment_by_id(vendor_payment_id, session)


        if vendor_payment_to_update is not None:
            vendor_payment_update_dict = update_data.model_dump()

            for k, v in vendor_payment_update_dict.items():
                setattr(vendor_payment_to_update, k, v)

            await session.commit()

            return vendor_payment_to_update
        else:
            return None  
        
    async def delete_vendor_payment(self, vendor_payment_id: str, session: AsyncSession):
        vendor_payment_to_delete = await self.get_vendor_payment_by_id(vendor_payment_id, session)

        if vendor_payment_to_delete is not None:
            await session.delete(vendor_payment_to_delete)
            await session.commit()

            return {}
        else:
            return None