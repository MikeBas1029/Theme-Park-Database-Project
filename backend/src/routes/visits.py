from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.visits import VisitService
from src.schemas.visits import Visit, VisitCreateModel, VisitUpdateModel

visit_router = APIRouter()
visit_service = VisitService()


@visit_router.get("/", response_model=List[Visit])
async def get_all_visits(session: AsyncSession = Depends(get_session)):
    visits = await visit_service.get_all_visits(session)
    return visits


@visit_router.get("/{visit_id}", response_model=Visit) 
async def get_visit(visit_id: str, session: AsyncSession = Depends(get_session)):
    visit = await visit_service.get_visit_by_id(visit_id, session)
    
    if visit:
        return visit
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Visit with visit {visit_id} not found.") 



@visit_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Visit,
)
async def create_a_visit(
    visit_data: VisitCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await visit_service.create_visit(visit_data, session)
    except Exception as error:
        raise error



@visit_router.patch("/{visit_id}", response_model=Visit)
async def update_visit(
    visit_id: str,
    update_data: VisitUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_visit = await visit_service.update_visit(visit_id, update_data, session)

    if updated_visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Visit with visit {visit_id} not found.") 
    else:
        return updated_visit


@visit_router.delete(
    "/{visit_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_visit(visit_id: str, session: AsyncSession = Depends(get_session)):
    visit_to_delete = await visit_service.delete_visit(visit_id, session)
    
    if visit_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Visit with visit {visit_id} not found.") 
