from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.ticket_types import TicketTypes 
from src.schemas.ticket_types import TicketTypeInputModel, TicketTypeOutputModel

class TicketTypeService:
    async def get_all_ticket_types(self, session: AsyncSession):
        query = select(TicketTypes).order_by(TicketTypes.ticket_type_id)

        result = await session.exec(query)

        return result.all()
    
    async def get_ticket_type_by_id(self, ticket_type_id: str, session: AsyncSession):
        query = select(TicketTypes).where(TicketTypes.ticket_type_id == ticket_type_id)

        result = await session.exec(query)

        ticket_type = result.first()

        return ticket_type if ticket_type is not None else None 
    
    async def ticket_type_exists(self, ticket_type_id: str, session: AsyncSession):
        query = select(TicketTypes).where(TicketTypes.ticket_type_id == ticket_type_id)

        result = await session.exec(query)

        ticket_type = result.first()

        return bool(ticket_type)
    
    async def create_ticket_type(
            self,
            ticket_type_data: TicketTypeInputModel,
            session: AsyncSession
    ):
        ticket_type_data_dict = ticket_type_data.model_dump()

        new_ticket_type = TicketTypes(**ticket_type_data_dict)

        # First check if ticket_type exists already
        existing_ticket_type = await self.ticket_type_exists(new_ticket_type.ticket_type_id, session)

        if existing_ticket_type:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"TicketType with ticket_type_id {new_ticket_type.ticket_type_id} already exists.")
        else:
            session.add(new_ticket_type)

            await session.commit()

            return new_ticket_type
    

    async def update_ticket_type(
            self, 
            ticket_type_id: str,
            update_data: TicketTypeInputModel,
            session: AsyncSession
    ):
        ticket_type_to_update = await self.get_ticket_type_by_id(ticket_type_id, session)


        if ticket_type_to_update is not None:
            ticket_type_update_dict = update_data.model_dump()

            for k, v in ticket_type_update_dict.items():
                setattr(ticket_type_to_update, k, v)

            await session.commit()

            return ticket_type_to_update
        else:
            return None  
        
    async def delete_ticket_type(self, ticket_type_id: str, session: AsyncSession):
        ticket_type_to_delete = await self.get_ticket_type_by_id(ticket_type_id, session)

        if ticket_type_to_delete is not None:
            await session.delete(ticket_type_to_delete)
            await session.commit()

            return {}
        else:
            return None