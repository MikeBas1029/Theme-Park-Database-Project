from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 

from src.models.department_managers import DepartmentManagers
from src.schemas.department_managers import DepartmentManagersModel


class DepartmentManagerService:
    async def get_all_department_managers(self, session: AsyncSession):
        query = select(DepartmentManagers).order_by(DepartmentManagers.department_id)

        result = await session.exec(query)

        return result.all()
    
    async def get_department_manager_by_id(self, department_id: int, employee_id: str, session: AsyncSession):
        query = select(DepartmentManagers).where(
            DepartmentManagers.department_id == department_id,
            DepartmentManagers.employee_id == employee_id)

        result = await session.exec(query)

        department_manager = result.first()

        return department_manager if department_manager is not None else None 
    
    async def department_manager_exists(self, department_id: int, employee_id: str, session: AsyncSession):
        query = select(DepartmentManagers).where(
            DepartmentManagers.department_id == department_id,
            DepartmentManagers.employee_id == employee_id
            )

        result = await session.exec(query)

        department_manager = result.first()

        return bool(department_manager)
    
    async def create_department_manager(
            self,
            dept_data: DepartmentManagersModel,
            session: AsyncSession
    ):
        dept_data_dict = dept_data.model_dump()

        new_dept_manager = DepartmentManagers(**dept_data_dict)

        # First check if department_manager exists already
        existing_department_manager = await self.department_manager_exists(new_dept_manager.department_id, new_dept_manager.employee_id, session)

        if existing_department_manager:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Department ID and manager ID already exists.")
        else:
            session.add(new_dept_manager)

            await session.commit()

            return new_dept_manager
    

    async def update_dept_manager(
            self, 
            department_id: int,
            employee_id: str,
            update_data: DepartmentManagersModel,
            session: AsyncSession
    ):
        dept_to_update = await self.get_department_manager_by_id(department_id, employee_id, session)


        if dept_to_update is not None:
            dept_update_dict = update_data.model_dump()

            for k, v in dept_update_dict.items():
                setattr(dept_to_update, k, v)

            await session.commit()

            return dept_to_update
        else:
            return None  
        
    async def delete_dept_manager(self, department_id: int, employee_id: str, session: AsyncSession):
        dept_to_delete = await self.get_department_manager_by_id(department_id, employee_id, session)

        if dept_to_delete is not None:
            await session.delete(dept_to_delete)
            await session.commit()

            return {}
        else:
            return None