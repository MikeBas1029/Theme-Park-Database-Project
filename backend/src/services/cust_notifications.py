from datetime import date
from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 

from src.models.cust_notifications import CustomerNotifications
from src.schemas.cust_notifications import CustomerNotificationInputModel, CustomerNotificationOutputModel


class CustomerNotificationService:
    async def get_all_cust_notifications(self, session: AsyncSession):
        query = select(CustomerNotifications).order_by(CustomerNotifications.date_created)

        result = await session.exec(query)

        return result.all()
    
    async def get_cust_notification_by_notif_id(self, notification_id: str, session: AsyncSession):
        query = select(CustomerNotifications).where(CustomerNotifications.notification_id == notification_id)

        result = await session.exec(query)

        cust_notification = result.first()

        return cust_notification if cust_notification is not None else None 
    
    async def get_cust_notification_by_customer_id(self, customer_id: str, session: AsyncSession):
        query = select(CustomerNotifications).where(CustomerNotifications.customer_id == customer_id)

        result = await session.exec(query)

        cust_notification = result.first()

        return cust_notification if cust_notification is not None else None 
    
    async def cust_notification_exists(self, notification_id: str, session: AsyncSession):
        query = select(CustomerNotifications).where(CustomerNotifications.notification_id == notification_id)

        result = await session.exec(query)

        cust_notification = result.first()

        return bool(cust_notification)
    
    async def create_cust_notification(
            self,
            cust_notification_data: CustomerNotificationInputModel,
            session: AsyncSession
    ):
        cust_notification_data_dict = cust_notification_data.model_dump()

        cust_notification_data_dict['created_date'] = date.today()

        new_cust_notification = CustomerNotifications(**cust_notification_data_dict)

        # First check if cust_notification exists already
        existing_cust_notification = await self.cust_notification_exists(new_cust_notification.notification_id, session)

        if existing_cust_notification:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"CustomerNotification with id {new_cust_notification.notification_id} already exists.")
        else:
            session.add(new_cust_notification)

            await session.commit()

            return new_cust_notification
    

    async def update_cust_notification(
            self, 
            notification_id: str,
            update_data: CustomerNotificationInputModel,
            session: AsyncSession
    ):
        cust_notification_to_update = await self.get_cust_notification_by_id(notification_id, session)


        if cust_notification_to_update is not None:
            cust_notification_update_dict = update_data.model_dump()

            for k, v in cust_notification_update_dict.items():
                if k != 'created_on':
                    setattr(cust_notification_to_update, k, v)

            await session.commit()

            return cust_notification_to_update
        else:
            return None  
        
    async def delete_cust_notification(self, notification_id: str, session: AsyncSession):
        cust_notification_to_delete = await self.get_cust_notification_by_id(notification_id, session)

        if cust_notification_to_delete is not None:
            await session.delete(cust_notification_to_delete)
            await session.commit()

            return {}
        else:
            return None