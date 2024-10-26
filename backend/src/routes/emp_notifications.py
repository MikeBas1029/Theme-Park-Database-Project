from typing import List 
from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.emp_notifications import EmployeeNotificationService
from src.schemas.emp_notifications import EmployeeNotificationInputModel, EmployeeNotificationOutputModel

emp_notification_router = APIRouter()
emp_notification_service = EmployeeNotificationService()

@emp_notification_router.get("/", response_model=List[EmployeeNotificationOutputModel])
async def get_all_emp_notifications(session: AsyncSession = Depends(get_session)):
    emp_notifications = await emp_notification_service.get_all_emp_notifications(session)
    return emp_notifications


@emp_notification_router.get("/{notification_id}", response_model=EmployeeNotificationOutputModel) 
async def get_emp_notification(notification_id: str, session: AsyncSession = Depends(get_session)):
    emp_notification = await emp_notification_service.get_emp_notification_by_id(notification_id, session)
    
    if emp_notification:
        return emp_notification
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EmployeeNotification with email {notification_id} not found.") 



@emp_notification_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeNotificationOutputModel,
)
async def create_a_emp_notification(
    emp_data: EmployeeNotificationInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await emp_notification_service.create_emp_notification(emp_data, session)
    except Exception as error:
        raise error



@emp_notification_router.patch("/{notification_id}", response_model=EmployeeNotificationOutputModel)
async def update_emp_notification(
    notification_id: str,
    update_data: EmployeeNotificationInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_emp_notification = await emp_notification_service.update_emp_notification(notification_id, update_data, session)

    if updated_emp_notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EmployeeNotification with email {notification_id} not found.") 
    else:
        return updated_emp_notification


@emp_notification_router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_emp_notification(notification_id: str, session: AsyncSession = Depends(get_session)):
    emp_notification_to_delete = await emp_notification_service.delete_emp_notification(notification_id, session)
    
    if emp_notification_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EmployeeNotification with email {notification_id} not found.") 
