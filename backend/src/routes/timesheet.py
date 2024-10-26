from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.timesheet import TimesheetService
from src.schemas.timesheet import TimesheetOutputModel, TimesheetCreateModel, TimesheetUpdateModel

timesheet_router = APIRouter()
timesheet_service = TimesheetService()


@timesheet_router.get("/", response_model=List[TimesheetOutputModel])
async def get_all_timesheets(session: AsyncSession = Depends(get_session)):
    timesheets = await timesheet_service.get_all_timesheets(session)
    return timesheets


@timesheet_router.get("/{timesheet_id}", response_model=TimesheetOutputModel) 
async def get_timesheet(timesheet_id: str, session: AsyncSession = Depends(get_session)):
    timesheet = await timesheet_service.get_timesheet_by_id(timesheet_id, session)
    
    if timesheet:
        return timesheet
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Timesheet with timesheet_id {timesheet_id} not found.") 



@timesheet_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TimesheetOutputModel,
)
async def create_a_timesheet(
    timesheet_data: TimesheetCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await timesheet_service.create_timesheet(timesheet_data, session)
    except Exception as error:
        raise error



@timesheet_router.patch("/{timesheet_id}", response_model=TimesheetOutputModel)
async def update_timesheet(
    timesheet_id: str,
    update_data: TimesheetUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_timesheet = await timesheet_service.update_timesheet(timesheet_id, update_data, session)

    if updated_timesheet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Timesheet with timesheet_id {timesheet_id} not found.") 
    else:
        return updated_timesheet


@timesheet_router.delete(
    "/{timesheet_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_timesheet(timesheet_id: str, session: AsyncSession = Depends(get_session)):
    timesheet_to_delete = await timesheet_service.delete_timesheet(timesheet_id, session)
    
    if timesheet_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Timesheet with timesheet_id {timesheet_id} not found.") 
