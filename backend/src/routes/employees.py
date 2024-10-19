from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.employees import EmployeeService
from src.schemas.employees import Employee, EmployeeCreateModel, EmployeeUpdateModel

employee_router = APIRouter()
employee_service = EmployeeService()


@employee_router.get("/", response_model=List[Employee])
async def get_all_employees(session: AsyncSession = Depends(get_session)):
    employees = await employee_service.get_all_employees(session)
    return employees


@employee_router.get("/{emp_id}", response_model=Employee) 
async def get_employee(emp_id: str, session: AsyncSession = Depends(get_session)):
    employee = await employee_service.get_employee_by_id(emp_id, session)
    
    if employee:
        return employee
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with email {emp_id} not found.") 



@employee_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeCreateModel,
)
async def create_a_employee(
    cust_data: EmployeeCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await employee_service.create_employee(cust_data, session)
    except Exception as error:
        raise error



@employee_router.patch("/{emp_id}", response_model=EmployeeUpdateModel)
async def update_employee(
    emp_id: str,
    update_data: EmployeeUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_employee = await employee_service.update_emp(emp_id, update_data, session)

    if updated_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with email {emp_id} not found.") 
    else:
        return updated_employee


@employee_router.delete(
    "/{emp_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee(emp_id: str, session: AsyncSession = Depends(get_session)):
    employee_to_delete = await employee_service.delete_emp(emp_id, session)
    
    if employee_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with email {emp_id} not found.") 
