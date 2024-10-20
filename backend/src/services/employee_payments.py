from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 

from src.models.employee_payments import EmployeePayments
from src.schemas.employee_payments import EmployeePaymentInputModel, EmployeePaymentOutputModel


class EmployeePaymentService:
    async def get_all_employee_payments(self, session: AsyncSession):
        query = select(EmployeePayments).order_by(EmployeePayments.payment_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_employee_payment_by_id(self, payment_id: int, session: AsyncSession):
        query = select(EmployeePayments).where(EmployeePayments.employee_payment_id == payment_id)

        result = await session.exec(query)

        employee_payment = result.first()

        return employee_payment if employee_payment is not None else None 
    
    async def employee_payment_exists(self, payment_id: int, session: AsyncSession):
        query = select(EmployeePayments).where(EmployeePayments.employee_payment_id == payment_id)

        result = await session.exec(query)

        employee_payment = result.first()

        return bool(employee_payment)
    
    async def create_employee_payment(
            self,
            payment_data: EmployeePaymentInputModel,
            session: AsyncSession
    ):
        payment_data_dict = payment_data.model_dump()

        new_payment = EmployeePayments(**payment_data_dict)

        # First check if employee_payment exists already
        existing_employee_payment = await self.employee_payment_exists(new_payment.employee_payment_id, session)

        if existing_employee_payment:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"EmployeePayment with id {new_payment.employee_payment_id} already exists.")
        else:
            session.add(new_payment)

            await session.commit()

            return new_payment
    

    async def update_payment(
            self, 
            payment_id: int,
            update_data: EmployeePaymentInputModel,
            session: AsyncSession
    ):
        payment_to_update = await self.get_employee_payment_by_id(payment_id, session)


        if payment_to_update is not None:
            payment_update_dict = update_data.model_dump()

            for k, v in payment_update_dict.items():
                setattr(payment_to_update, k, v)

            await session.commit()

            return payment_to_update
        else:
            return None  
        
    async def delete_payment(self, payment_id: int, session: AsyncSession):
        payment_to_delete = await self.get_employee_payment_by_id(payment_id, session)

        if payment_to_delete is not None:
            await session.delete(payment_to_delete)
            await session.commit()

            return {}
        else:
            return None