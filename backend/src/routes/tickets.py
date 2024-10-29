from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.tickets import TicketService
from src.schemas.tickets import TicketOutputModel, TicketCreateModel, TicketUpdateModel

ticket_router = APIRouter()
ticket_service = TicketService()


@ticket_router.get("/", response_model=List[TicketOutputModel])
async def get_all_tickets(session: AsyncSession = Depends(get_session)):
    tickets = await ticket_service.get_all_tickets(session)
    return tickets


@ticket_router.get("/ticket/{ticket_id}", response_model=TicketOutputModel) 
async def get_ticket(ticket_id: str, session: AsyncSession = Depends(get_session)):
    ticket = await ticket_service.get_ticket_by_id(ticket_id, session)
    
    if ticket:
        return ticket
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with ticket_id {ticket_id} not found.") 


@ticket_router.get("/user/{user_id}", response_model=List[TicketOutputModel]) 
async def get_ticket(user_id: str, session: AsyncSession = Depends(get_session)):
    tickets = await ticket_service.get_ticket_by_user_id(user_id, session)
    
    return tickets


@ticket_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TicketOutputModel,
)
async def create_a_ticket(
    ticket_data: TicketCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await ticket_service.create_ticket(ticket_data, session)
    except Exception as error:
        raise error



@ticket_router.patch("/{ticket_id}", response_model=TicketOutputModel)
async def update_ticket(
    ticket_id: str,
    update_data: TicketUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_ticket = await ticket_service.update_ticket(ticket_id, update_data, session)

    if updated_ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with ticket_id {ticket_id} not found.") 
    else:
        return updated_ticket


@ticket_router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ticket(ticket_id: str, session: AsyncSession = Depends(get_session)):
    ticket_to_delete = await ticket_service.delete_ticket(ticket_id, session)
    
    if ticket_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with ticket_id {ticket_id} not found.") 
