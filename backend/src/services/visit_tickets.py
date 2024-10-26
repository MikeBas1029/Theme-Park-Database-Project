from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.visit_tickets import VisitTickets
from src.schemas.visit_tickets import VisitTicketInputModel


class VisitTicketService:
    async def get_all_visit_tickets(self, session: AsyncSession):
        query = select(VisitTickets)

        result = await session.exec(query)

        return result.all()
    
    async def get_visit_ticket_by_id(self, visit_ticket_id: str, session: AsyncSession):
        query = select(VisitTickets).where(VisitTickets.visit_ticket_id == visit_ticket_id)

        result = await session.exec(query)

        visit_ticket = result.first()

        return visit_ticket if visit_ticket is not None else None 
    
    async def visit_ticket_exists(self, visit_ticket_id: str, session: AsyncSession):
        query = select(VisitTickets).where(VisitTickets.visit_ticket_id == visit_ticket_id)

        result = await session.exec(query)

        visit_ticket = result.first()

        return bool(visit_ticket)
    
    async def create_visit_ticket(
            self,
            visit_ticket_data: VisitTicketInputModel,
            session: AsyncSession
    ):
        visit_ticket_data_dict = visit_ticket_data.model_dump()

        new_visit_ticket = VisitTickets(**visit_ticket_data_dict)

        # First check if visit_ticket exists already
        existing_visit_ticket = await self.visit_ticket_exists(new_visit_ticket.visit_ticket_id, session)

        if existing_visit_ticket:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"VisitTicket with visit_ticket_id {new_visit_ticket.visit_ticket_id} already exists.")
        else:
            session.add(new_visit_ticket)

            await session.commit()

            return new_visit_ticket
    

    async def update_visit_ticket(
            self, 
            visit_ticket_id: str,
            update_data: VisitTicketInputModel,
            session: AsyncSession
    ):
        visit_ticket_to_update = await self.get_visit_ticket_by_id(visit_ticket_id, session)


        if visit_ticket_to_update is not None:
            visit_ticket_update_dict = update_data.model_dump()

            for k, v in visit_ticket_update_dict.items():
                setattr(visit_ticket_to_update, k, v)

            await session.commit()

            return visit_ticket_to_update
        else:
            return None  
        
    async def delete_visit_ticket(self, visit_ticket_id: str, session: AsyncSession):
        visit_ticket_to_delete = await self.get_visit_ticket_by_id(visit_ticket_id, session)

        if visit_ticket_to_delete is not None:
            await session.delete(visit_ticket_to_delete)
            await session.commit()

            return {}
        else:
            return None