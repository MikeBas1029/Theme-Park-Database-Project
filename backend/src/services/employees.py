from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 

from src.models.employees import Employees
from src.schemas.employees import EmployeeCreateModel, EmployeeUpdateModel


class EmployeeService:
    async def get_all_employees(self, session: AsyncSession):
        query = select(Employees).order_by(Employees.last_name)

        result = await session.exec(query)

        return result.all()
    
    async def get_employee_by_id(self, emp_id: str, session: AsyncSession):
        query = select(Employees).where(Employees.employee_id == emp_id)

        result = await session.exec(query)

        employee = result.first()

        return employee if employee is not None else None 
    
    async def employee_exists(self, emp_id: str, session: AsyncSession):
        query = select(Employees).where(Employees.employee_id == emp_id)

        result = await session.exec(query)

        employee = result.first()

        return bool(employee)
    
    async def create_employee(
            self,
            emp_data: EmployeeCreateModel,
            session: AsyncSession
    ):
        emp_data_dict = emp_data.model_dump()

        new_emp = Employees(**emp_data_dict)

        # First check if employee exists already
        existing_employee = await self.employee_exists(new_emp.employee_id, session)

        if existing_employee:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Employee with email {new_emp.employee_id} already exists.")
        else:
            session.add(new_emp)

            await session.commit()

            return new_emp
    

    async def update_emp(
            self, 
            emp_id: str,
            update_data: EmployeeUpdateModel,
            session: AsyncSession
    ):
        emp_to_update = await self.get_employee_by_id(emp_id, session)


        if emp_to_update is not None:
            emp_update_dict = update_data.model_dump()

            for k, v in emp_update_dict.items():
                setattr(emp_to_update, k, v)

            await session.commit()

            return emp_to_update
        else:
            return None  
        
    async def delete_emp(self, emp_id: str, session: AsyncSession):
        emp_to_delete = await self.get_employee_by_id(emp_id, session)

        if emp_to_delete is not None:
            await session.delete(emp_to_delete)
            await session.commit()

            return {}
        else:
            return None