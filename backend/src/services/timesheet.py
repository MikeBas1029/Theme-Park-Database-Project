from datetime import date
from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.timesheet import TimesheetStatus, Timesheet
from src.schemas.timesheet import TimesheetCreateModel, TimesheetUpdateModel, TimesheetStatus

class TimesheetService:
    async def get_all_timesheets(self, session: AsyncSession):
        query = select(Timesheet).order_by(Timesheet.created_on)

        result = await session.exec(query)

        return result.all()
    
    async def get_timesheet_by_id(self, timesheet_id: str, session: AsyncSession):
        query = select(Timesheet).where(Timesheet.shift_id == timesheet_id)

        result = await session.exec(query)

        timesheet = result.first()

        return timesheet if timesheet is not None else None 
    
    async def timesheet_exists(self, timesheet_id: str, session: AsyncSession):
        query = select(Timesheet).where(Timesheet.shift_id == timesheet_id)

        result = await session.exec(query)

        timesheet = result.first()

        return bool(timesheet)
    
    async def create_timesheet(
            self,
            timesheet_data: TimesheetCreateModel,
            session: AsyncSession
    ):
        timesheet_data_dict = timesheet_data.model_dump()

        timesheet_data_dict['created_on'] = date.today()
        timesheet_data_dict['updated_on'] = date.today()

        new_timesheet = Timesheet(**timesheet_data_dict)

        # First check if timesheet exists already
        existing_timesheet = await self.timesheet_exists(new_timesheet.shift_id, session)

        if existing_timesheet:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Timesheet with timesheet_id {new_timesheet.shift_id} already exists.")
        else:
            session.add(new_timesheet)

            await session.commit()

            return new_timesheet
    

    async def update_timesheet(
            self, 
            timesheet_id: str,
            update_data: TimesheetUpdateModel,
            session: AsyncSession
    ):
        timesheet_to_update = await self.get_timesheet_by_id(timesheet_id, session)

        if timesheet_to_update is not None:
            timesheet_update_dict = update_data.model_dump()

            timesheet_update_dict['created_on'] = timesheet_to_update.created_on
            timesheet_update_dict['updated_on'] = date.today()


            for k, v in timesheet_update_dict.items():
                if k != 'created_on':
                    setattr(timesheet_to_update, k, v)


            await session.commit()

            return timesheet_to_update
        else:
            return None  
        
    async def delete_timesheet(self, timesheet_id: str, session: AsyncSession):
        timesheet_to_delete = await self.get_timesheet_by_id(timesheet_id, session)

        if timesheet_to_delete is not None:
            await session.delete(timesheet_to_delete)
            await session.commit()

            return {}
        else:
            return None