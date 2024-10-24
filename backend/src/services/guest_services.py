from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.guest_services import GuestServices
from src.schemas.guest_services import GuestServiceInputModel


class GuestServicesService:
    async def get_all_guest_services(self, session: AsyncSession):
        query = select(GuestServices).order_by(GuestServices.service_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_guest_service_by_id(self, guest_service_id: str, session: AsyncSession):
        query = select(GuestServices).where(GuestServices.service_request_id == guest_service_id)

        result = await session.exec(query)

        guest_service = result.first()

        return guest_service if guest_service is not None else None 
    
    async def guest_service_exists(self, guest_service_id: str, session: AsyncSession):
        query = select(GuestServices).where(GuestServices.service_request_id == guest_service_id)

        result = await session.exec(query)

        guest_service = result.first()

        return bool(guest_service)
    
    async def create_guest_service(
            self,
            guest_service_data: GuestServiceInputModel,
            session: AsyncSession
    ):
        guest_service_data_dict = guest_service_data.model_dump()

        new_guest_service = GuestServices(**guest_service_data_dict)

        # First check if guest_service exists already
        existing_guest_service = await self.guest_service_exists(new_guest_service.service_request_id, session)

        if existing_guest_service:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Guest service with guest_service_id {new_guest_service.service_request_id} already exists.")
        else:
            session.add(new_guest_service)

            await session.commit()

            return new_guest_service
    

    async def update_guest_service(
            self, 
            guest_service_id: str,
            update_data: GuestServiceInputModel,
            session: AsyncSession
    ):
        guest_service_to_update = await self.get_guest_service_by_id(guest_service_id, session)


        if guest_service_to_update is not None:
            guest_service_update_dict = update_data.model_dump()

            for k, v in guest_service_update_dict.items():
                setattr(guest_service_to_update, k, v)

            await session.commit()

            return guest_service_to_update
        else:
            return None  
        
    async def delete_guest_service(self, guest_service_id: str, session: AsyncSession):
        guest_service_to_delete = await self.get_guest_service_by_id(guest_service_id, session)

        if guest_service_to_delete is not None:
            await session.delete(guest_service_to_delete)
            await session.commit()

            return {}
        else:
            return None