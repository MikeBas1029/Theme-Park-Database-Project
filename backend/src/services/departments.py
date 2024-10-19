from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 

from src.models.departments import Departments
from src.schemas.departments import DepartmentCreateModel, DepartmentUpdateModel


class DepartmentService:
    async def get_all_departments(self, session: AsyncSession):
        query = select(Departments).order_by(Departments.name)

        result = await session.exec(query)

        return result.all()
    
    async def get_department_by_id(self, dept_id: str, session: AsyncSession):
        query = select(Departments).where(Departments.department_id == dept_id)

        result = await session.exec(query)

        department = result.first()

        return department if department is not None else None 
    
    async def department_exists(self, dept_id: str, session: AsyncSession):
        query = select(Departments).where(Departments.department_id == dept_id)

        result = await session.exec(query)

        department = result.first()

        return bool(department)
    
    async def create_department(
            self,
            dept_data: DepartmentCreateModel,
            session: AsyncSession
    ):
        dept_data_dict = dept_data.model_dump()

        new_dept = Departments(**dept_data_dict)

        # First check if department exists already
        existing_department = await self.department_exists(new_dept.department_id, session)

        if existing_department:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Department with id {new_dept.department_id} already exists.")
        else:
            session.add(new_dept)

            await session.commit()

            return new_dept
    

    async def update_dept(
            self, 
            dept_id: str,
            update_data: DepartmentUpdateModel,
            session: AsyncSession
    ):
        dept_to_update = await self.get_department_by_id(dept_id, session)


        if dept_to_update is not None:
            dept_update_dict = update_data.model_dump()

            for k, v in dept_update_dict.items():
                setattr(dept_to_update, k, v)

            await session.commit()

            return dept_to_update
        else:
            return None  
        
    async def delete_dept(self, dept_id: str, session: AsyncSession):
        dept_to_delete = await self.get_department_by_id(dept_id, session)

        if dept_to_delete is not None:
            await session.delete(dept_to_delete)
            await session.commit()

            return {}
        else:
            return None