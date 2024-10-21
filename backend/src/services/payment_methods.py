from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 

from src.models.payment_methods import PaymentMethods
from src.schemas.payment_methods import PaymentMethodInputModel, PaymentMethodOutputModel


class PaymentMethodService:
    async def get_all_payment_methods(self, session: AsyncSession):
        query = select(PaymentMethods).order_by(PaymentMethods.method_type)

        result = await session.exec(query)

        return result.all()
    
    async def get_payment_method_by_id(self, method_id: int, session: AsyncSession):
        query = select(PaymentMethods).where(PaymentMethods.payment_method_id == method_id)

        result = await session.exec(query)

        payment_method = result.first()

        return payment_method if payment_method is not None else None 
    
    async def payment_method_exists(self, method_id: int, session: AsyncSession):
        query = select(PaymentMethods).where(PaymentMethods.payment_method_id == method_id)

        result = await session.exec(query)

        payment_method = result.first()

        return bool(payment_method)
    
    async def create_payment_method(
            self,
            payment_data: PaymentMethodInputModel,
            session: AsyncSession
    ):
        payment_data_dict = payment_data.model_dump()

        new_payment = PaymentMethods(**payment_data_dict)

        # First check if payment_method exists already
        existing_payment_method = await self.payment_method_exists(new_payment.payment_method_id, session)

        if existing_payment_method:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"PaymentMethod with id {new_payment.payment_method_id} already exists.")
        else:
            session.add(new_payment)

            await session.commit()

            return new_payment
    

    async def update_payment(
            self, 
            method_id: int,
            update_data: PaymentMethodInputModel,
            session: AsyncSession
    ):
        payment_to_update = await self.get_payment_method_by_id(method_id, session)


        if payment_to_update is not None:
            payment_update_dict = update_data.model_dump()

            for k, v in payment_update_dict.items():
                setattr(payment_to_update, k, v)

            await session.commit()

            return payment_to_update
        else:
            return None  
        
    async def delete_payment(self, method_id: int, session: AsyncSession):
        payment_to_delete = await self.get_payment_method_by_id(method_id, session)

        if payment_to_delete is not None:
            await session.delete(payment_to_delete)
            await session.commit()

            return {}
        else:
            return None