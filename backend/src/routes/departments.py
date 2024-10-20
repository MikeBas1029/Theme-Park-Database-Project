from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.departments import DepartmentService
from src.schemas.departments import Department, DepartmentCreateModel, DepartmentUpdateModel

department_router = APIRouter()
department_service = DepartmentService()


@department_router.get("/", response_model=List[Department])
async def get_all_departments(session: AsyncSession = Depends(get_session)):
    departments = await department_service.get_all_departments(session)
    return departments


@department_router.get("/{dept_id}", response_model=Department) 
async def get_department(dept_id: str, session: AsyncSession = Depends(get_session)):
    department = await department_service.get_department_by_id(dept_id, session)
    
    if department:
        return department
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Department with email {dept_id} not found.") 



@department_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Department,
)
async def create_a_department(
    dept_data: DepartmentCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await department_service.create_department(dept_data, session)
    except Exception as error:
        raise error



@department_router.patch("/{dept_id}", response_model=Department)
async def update_department(
    dept_id: str,
    update_data: DepartmentUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_department = await department_service.update_dept(dept_id, update_data, session)

    if updated_department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Department with email {dept_id} not found.") 
    else:
        return updated_department


@department_router.delete(
    "/{dept_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_department(dept_id: str, session: AsyncSession = Depends(get_session)):
    department_to_delete = await department_service.delete_dept(dept_id, session)
    
    if department_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with email {dept_id} not found.") 
