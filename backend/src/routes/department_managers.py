from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.department_managers import DepartmentManagerService
from src.schemas.department_managers import DepartmentManagersModel

department_manager_router = APIRouter()
department_manager_service = DepartmentManagerService()


@department_manager_router.get("/", response_model=List[DepartmentManagersModel])
async def get_all_department_managers(session: AsyncSession = Depends(get_session)):
    department_manages = await department_manager_service.get_all_department_managers(session)
    return department_manages


@department_manager_router.get("/{dept_id}/{employee_id}", response_model=DepartmentManagersModel) 
async def get_department_manager(
    dept_id: int, 
    employee_id: str,
    session: AsyncSession = Depends(get_session)):
    department_manager = await department_manager_service.get_department_manager_by_id(dept_id, employee_id, session)
    
    if department_manager:
        return department_manager
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Department manager not found.") 



@department_manager_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DepartmentManagersModel,
)
async def create_a_department_manager(
    dept_data: DepartmentManagersModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await department_manager_service.create_department_manager(dept_data, session)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not create department manager. {error}")



@department_manager_router.patch("/{dept_id}/{employee_id}", response_model=DepartmentManagersModel)
async def update_department_manager(
    dept_id: int,
    employee_id: str,
    update_data: DepartmentManagersModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_department_manager = await department_manager_service.update_dept_manager(dept_id, employee_id, update_data, session)

    if updated_department_manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Department manager with ID {employee_id} not found for department {dept_id}.") 
    else:
        return updated_department_manager


@department_manager_router.delete(
    "/{dept_id}/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_department_manager(dept_id: int, employee_id: str, session: AsyncSession = Depends(get_session)):
    department_manager_to_delete = await department_manager_service.delete_dept_manager(dept_id, employee_id, session)
    
    if department_manager_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Department manager with ID {employee_id} not found for department {dept_id}.") 
