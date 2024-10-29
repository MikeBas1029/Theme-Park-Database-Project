from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.tickets import Tickets 
from src.schemas.tickets import TicketCreateModel, TicketUpdateModel, TicketStatus

class TicketService:
    async def get_all_tickets(self, session: AsyncSession):
        query = select(Tickets).order_by(Tickets.purchase_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_ticket_by_id(self, ticket_id: str, session: AsyncSession):
        query = select(Tickets).where(Tickets.ticket_id == ticket_id)

        result = await session.exec(query)

        ticket = result.first()

        return ticket if ticket is not None else None 
    
    async def get_ticket_by_user_id(self, user_id: str, session: AsyncSession) -> list:
        query = select(Tickets).where(Tickets.customer_id == user_id)

        result = await session.exec(query)

        tickets = result.all()

        return tickets
    
    async def ticket_exists(self, ticket_id: str, session: AsyncSession):
        query = select(Tickets).where(Tickets.ticket_id == ticket_id)

        result = await session.exec(query)

        ticket = result.first()

        return bool(ticket)
    
    async def create_ticket(
            self,
            ticket_data: TicketCreateModel,
            session: AsyncSession
    ):
        ticket_data_dict = ticket_data.model_dump()

        ticket_data_dict['status'] = TicketStatus.ACTIVE.value

        new_ticket = Tickets(**ticket_data_dict)

        # First check if ticket exists already
        existing_ticket = await self.ticket_exists(new_ticket.ticket_id, session)

        if existing_ticket:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ticket with ticket_id {new_ticket.ticket_id} already exists.")
        else:
            session.add(new_ticket)

            await session.commit()

            return new_ticket
    

    async def update_ticket(
            self, 
            ticket_id: str,
            update_data: TicketUpdateModel,
            session: AsyncSession
    ):
        ticket_to_update = await self.get_ticket_by_id(ticket_id, session)


        if ticket_to_update is not None:
            ticket_update_dict = update_data.model_dump()

            for k, v in ticket_update_dict.items():
                setattr(ticket_to_update, k, v)

            await session.commit()

            return ticket_to_update
        else:
            return None  
        
    async def delete_ticket(self, ticket_id: str, session: AsyncSession):
        ticket_to_delete = await self.get_ticket_by_id(ticket_id, session)

        if ticket_to_delete is not None:
            await session.delete(ticket_to_delete)
            await session.commit()

            return {}
        else:
            return None