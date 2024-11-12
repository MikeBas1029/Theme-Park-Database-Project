from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.ticket_types import TicketTypeService
from src.schemas.ticket_types import TicketTypeOutputModel, TicketTypeInputModel

ticket_type_router = APIRouter()
ticket_type_service = TicketTypeService()


@ticket_type_router.get("/", response_model=List[TicketTypeOutputModel])
async def get_all_ticket_types(session: AsyncSession = Depends(get_session)):
    ticket_types = await ticket_type_service.get_all_ticket_types(session)
    return ticket_types


@ticket_type_router.get("/{ticket_type_id}", response_model=TicketTypeOutputModel) 
async def get_ticket_type(ticket_type_id: str, session: AsyncSession = Depends(get_session)):
    ticket_type = await ticket_type_service.get_ticket_type_by_id(ticket_type_id, session)
    
    if ticket_type:
        return ticket_type
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TicketType with ticket_type_id {ticket_type_id} not found.") 



@ticket_type_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TicketTypeOutputModel,
)
async def create_a_ticket_type(
    ticket_type_data: TicketTypeInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await ticket_type_service.create_ticket_type(ticket_type_data, session)
    except Exception as error:
        raise error



@ticket_type_router.patch("/{ticket_type_id}", response_model=TicketTypeOutputModel)
async def update_ticket_type(
    ticket_type_id: str,
    update_data: TicketTypeOutputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_ticket_type = await ticket_type_service.update_ticket_type(ticket_type_id, update_data, session)

    if updated_ticket_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TicketType with ticket_type_id {ticket_type_id} not found.") 
    else:
        return updated_ticket_type


@ticket_type_router.delete(
    "/{ticket_type_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_ticket_type(ticket_type_id: str, session: AsyncSession = Depends(get_session)):
    ticket_type_to_delete = await ticket_type_service.delete_ticket_type(ticket_type_id, session)
    
    if ticket_type_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"TicketType with ticket_type_id {ticket_type_id} not found.") 
