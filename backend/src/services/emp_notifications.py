from datetime import date
from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status 

from src.models.emp_notifications import EmployeeNotifications
from src.schemas.emp_notifications import EmployeeNotificationInputModel, EmployeeNotificationOutputModel


class EmployeeNotificationService:
    async def get_all_emp_notifications(self, session: AsyncSession):
        query = select(EmployeeNotifications).order_by(EmployeeNotifications.date_created)

        result = await session.exec(query)

        return result.all()
    
    async def get_emp_notification_by_id(self, notification_id: str, session: AsyncSession):
        query = select(EmployeeNotifications).where(EmployeeNotifications.notification_id == notification_id)

        result = await session.exec(query)

        emp_notification = result.first()

        return emp_notification if emp_notification is not None else None 
    
    async def emp_notification_exists(self, notification_id: str, session: AsyncSession):
        query = select(EmployeeNotifications).where(EmployeeNotifications.notification_id == notification_id)

        result = await session.exec(query)

        emp_notification = result.first()

        return bool(emp_notification)
    
    async def create_emp_notification(
            self,
            emp_notification_data: EmployeeNotificationInputModel,
            session: AsyncSession
    ):
        emp_notification_data_dict = emp_notification_data.model_dump()

        emp_notification_data_dict['created_date'] = date.today()

        new_emp_notification = EmployeeNotifications(**emp_notification_data_dict)

        # First check if emp_notification exists already
        existing_emp_notification = await self.emp_notification_exists(new_emp_notification.notification_id, session)

        if existing_emp_notification:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"EmployeeNotification with id {new_emp_notification.notification_id} already exists.")
        else:
            session.add(new_emp_notification)

            await session.commit()

            return new_emp_notification
    

    async def update_emp_notification(
            self, 
            notification_id: str,
            update_data: EmployeeNotificationInputModel,
            session: AsyncSession
    ):
        emp_notification_to_update = await self.get_emp_notification_by_id(notification_id, session)


        if emp_notification_to_update is not None:
            emp_notification_update_dict = update_data.model_dump()

            for k, v in emp_notification_update_dict.items():
                if k != 'created_on':
                    setattr(emp_notification_to_update, k, v)

            await session.commit()

            return emp_notification_to_update
        else:
            return None  
        
    async def delete_emp_notification(self, notification_id: str, session: AsyncSession):
        emp_notification_to_delete = await self.get_emp_notification_by_id(notification_id, session)

        if emp_notification_to_delete is not None:
            await session.delete(emp_notification_to_delete)
            await session.commit()

            return {}
        else:
            return None