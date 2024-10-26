from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.visit_tickets import VisitTicketService
from src.schemas.visit_tickets import VisitTicketInputModel, VisitTicketOutputModel

visit_ticket_router = APIRouter()
visit_ticket_service = VisitTicketService()


@visit_ticket_router.get("/", response_model=List[VisitTicketOutputModel])
async def get_all_visit_tickets(session: AsyncSession = Depends(get_session)):
    visit_ticket = await visit_ticket_service.get_all_visit_tickets(session)
    return visit_ticket


@visit_ticket_router.get("/{visit_ticket_id}", response_model=VisitTicketOutputModel) 
async def get_visit_ticket(visit_ticket_id: str, session: AsyncSession = Depends(get_session)):
    visit_ticket = await visit_ticket_service.get_visit_ticket_by_id(visit_ticket_id, session)
    
    if visit_ticket:
        return visit_ticket
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with visit_ticket id {visit_ticket_id} not found.") 



@visit_ticket_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=VisitTicketOutputModel,
)
async def create_a_visit_ticket(
    visit_ticket_data: VisitTicketInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await visit_ticket_service.create_visit_ticket(visit_ticket_data, session)
    except Exception as error:
        raise error



@visit_ticket_router.patch("/{visit_ticket_id}", response_model=VisitTicketOutputModel)
async def update_visit_ticket(
    visit_ticket_id: str,
    update_data: VisitTicketInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_visit_ticket = await visit_ticket_service.update_visit_ticket(visit_ticket_id, update_data, session)

    if updated_visit_ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with visit_ticket id {visit_ticket_id} not found.") 
    else:
        return updated_visit_ticket


@visit_ticket_router.delete(
    "/{visit_ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_visit_ticket(visit_ticket_id: str, session: AsyncSession = Depends(get_session)):
    visit_ticket_to_delete = await visit_ticket_service.delete_visit_ticket(visit_ticket_id, session)
    
    if visit_ticket_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor Payment with visit_ticket id {visit_ticket_id} not found.") 
