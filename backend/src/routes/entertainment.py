from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.entertainment import EntertainmentService
from src.schemas.entertainment import EntertainmentInputModel, EntertainmentOutputModel

entertainment_router = APIRouter()
entertainment_service = EntertainmentService()


@entertainment_router.get("/", response_model=List[EntertainmentOutputModel])
async def get_all_entertainment(session: AsyncSession = Depends(get_session)):
    entertainment = await entertainment_service.get_all_entertainment(session)
    return entertainment


@entertainment_router.get("/{entertainment_id}", response_model=EntertainmentOutputModel) 
async def get_entertainment(entertainment_id: str, session: AsyncSession = Depends(get_session)):
    entertainment = await entertainment_service.get_show_by_id(entertainment_id, session)
    
    if entertainment:
        return entertainment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entertainment with entertainment {entertainment_id} not found.") 



@entertainment_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EntertainmentOutputModel,
)
async def create_a_entertainment(
    entertainment_data: EntertainmentInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await entertainment_service.create_show(entertainment_data, session)
    except Exception as error:
        raise error



@entertainment_router.patch("/{entertainment_id}", response_model=EntertainmentOutputModel)
async def update_entertainment(
    entertainment_id: str,
    update_data: EntertainmentInputModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_entertainment = await entertainment_service.update_show(entertainment_id, update_data, session)

    if updated_entertainment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entertainment with entertainment {entertainment_id} not found.") 
    else:
        return updated_entertainment


@entertainment_router.delete(
    "/{entertainment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_entertainment(entertainment_id: str, session: AsyncSession = Depends(get_session)):
    entertainment_to_delete = await entertainment_service.delete_show(entertainment_id, session)
    
    if entertainment_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entertainment with entertainment {entertainment_id} not found.") 
