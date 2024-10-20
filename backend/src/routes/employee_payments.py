from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.employee_payments import EmployeePaymentService
from src.schemas.employee_payments import EmployeePaymentInputModel, EmployeePaymentOutputModel

employee_payment_router = APIRouter()
employee_payment_service = EmployeePaymentService()


@employee_payment_router.get("/", response_model=List[EmployeePaymentOutputModel])
async def get_all_employee_payments(session: AsyncSession = Depends(get_session)):
    employee_payments = await employee_payment_service.get_all_employee_payments(session)
    return employee_payments


@employee_payment_router.get("/{payment_id}", response_model=EmployeePaymentOutputModel) 
async def get_employee_payment(payment_id: int, session: AsyncSession = Depends(get_session)):
    employee_payment = await employee_payment_service.get_employee_payment_by_id(payment_id, session)
    
    if employee_payment:
        return employee_payment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee payment record with payment id {payment_id} not found.") 



@employee_payment_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeePaymentOutputModel,
)
async def create_a_employee_payment(
    payment_data: EmployeePaymentInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await employee_payment_service.create_employee_payment(payment_data, session)
    except Exception as error:
        raise error



@employee_payment_router.patch("/{payment_id}", response_model=EmployeePaymentOutputModel)
async def update_employee_payment(
    payment_id: int,
    update_data: EmployeePaymentInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_employee_payment = await employee_payment_service.update_payment(payment_id, update_data, session)

    if updated_employee_payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee payment record with payment id {payment_id} not found.") 
    else:
        return updated_employee_payment


@employee_payment_router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee_payment(payment_id: int, session: AsyncSession = Depends(get_session)):
    employee_payment_to_delete = await employee_payment_service.delete_payment(payment_id, session)
    
    if employee_payment_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee payment record with payment id {payment_id} not found.") 
