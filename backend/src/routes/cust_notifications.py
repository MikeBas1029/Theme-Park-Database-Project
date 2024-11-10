from typing import List 
from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.cust_notifications import CustomerNotificationService
from src.schemas.cust_notifications import CustomerNotificationInputModel, CustomerNotificationOutputModel

cust_notification_router = APIRouter()
cust_notification_service = CustomerNotificationService()

@cust_notification_router.get("/", response_model=List[CustomerNotificationOutputModel])
async def get_all_cust_notifications(session: AsyncSession = Depends(get_session)):
    cust_notifications = await cust_notification_service.get_all_cust_notifications(session)
    return cust_notifications


@cust_notification_router.get("/notif/{notification_id}", response_model=CustomerNotificationOutputModel) 
async def get_cust_notification_by_notif_id(notification_id: str, session: AsyncSession = Depends(get_session)):
    cust_notification = await cust_notification_service.get_cust_notification_by_notif_id(notification_id, session)
    
    if cust_notification:
        return cust_notification
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No notification found for notification with ID {notification_id}.") 


@cust_notification_router.get("/cust/{customer_id}", response_model=List[CustomerNotificationOutputModel]) 
async def get_cust_notification_by_cust_id(customer_id: str, session: AsyncSession = Depends(get_session)):
    cust_notification = await cust_notification_service.get_cust_notification_by_customer_id(customer_id, session)
    
    if cust_notification:
        return cust_notification
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No notification found for customer with ID {customer_id}.") 



@cust_notification_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerNotificationOutputModel,
)
async def create_a_cust_notification(
    cust_data: CustomerNotificationInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await cust_notification_service.create_cust_notification(cust_data, session)
    except Exception as error:
        raise error



@cust_notification_router.patch("/{notification_id}", response_model=CustomerNotificationOutputModel)
async def update_cust_notification(
    notification_id: str,
    update_data: CustomerNotificationInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_cust_notification = await cust_notification_service.update_cust_notification(notification_id, update_data, session)

    if updated_cust_notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CustomerNotification with email {notification_id} not found.") 
    else:
        return updated_cust_notification


@cust_notification_router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_cust_notification(notification_id: str, session: AsyncSession = Depends(get_session)):
    cust_notification_to_delete = await cust_notification_service.delete_cust_notification(notification_id, session)
    
    if cust_notification_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"CustomerNotification with email {notification_id} not found.") 
