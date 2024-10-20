from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.sections import SectionService
from src.schemas.sections import Section, SectionCreateModel, SectionUpdateModel

section_router = APIRouter()
section_service = SectionService()


@section_router.get("/", response_model=List[Section])
async def get_all_sections(session: AsyncSession = Depends(get_session)):
    sections = await section_service.get_all_sections(session)
    return sections


@section_router.get("/{section_id}", response_model=Section) 
async def get_section(section_id: str, session: AsyncSession = Depends(get_session)):
    section = await section_service.get_section_by_id(section_id, session)
    
    if section:
        return section
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Section with section_id {section_id} not found.") 



@section_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Section,
)
async def create_a_section(
    section_data: SectionCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await section_service.create_section(section_data, session)
    except Exception as error:
        raise error



@section_router.patch("/{section_id}", response_model=Section)
async def update_section(
    section_id: str,
    update_data: SectionUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_section = await section_service.update_section(section_id, update_data, session)

    if updated_section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Section with section_id {section_id} not found.") 
    else:
        return updated_section


@section_router.delete(
    "/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_section(section_id: str, session: AsyncSession = Depends(get_session)):
    section_to_delete = await section_service.delete_section(section_id, session)
    
    if section_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Section with section_id {section_id} not found.") 
