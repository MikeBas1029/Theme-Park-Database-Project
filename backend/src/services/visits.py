from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.visits import Visits 
from src.schemas.visits import VisitInputModel

class VisitService:
    async def get_all_visits(self, session: AsyncSession):
        query = select(Visits).order_by(Visits.visit_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_visit_by_id(self, visit_id: str, session: AsyncSession):
        query = select(Visits).where(Visits.visit_id == visit_id)

        result = await session.exec(query)

        visit = result.first()

        return visit if visit is not None else None 
    
    async def visit_exists(self, visit_id: str, session: AsyncSession):
        query = select(Visits).where(Visits.visit_id == visit_id)

        result = await session.exec(query)

        visit = result.first()

        return bool(visit)
    
    async def create_visit(
            self,
            visit_data: VisitInputModel,
            session: AsyncSession
    ):
        visit_data_dict = visit_data.model_dump()

        new_visit = Visits(**visit_data_dict)

        # First check if visit exists already
        existing_visit = await self.visit_exists(new_visit.visit_id, session)

        if existing_visit:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Visit with visit_id {new_visit.visit_id} already exists.")
        else:
            session.add(new_visit)

            await session.commit()

            return new_visit
    

    async def update_visit(
            self, 
            visit_id: str,
            update_data: VisitInputModel,
            session: AsyncSession
    ):
        visit_to_update = await self.get_visit_by_id(visit_id, session)


        if visit_to_update is not None:
            visit_update_dict = update_data.model_dump()

            for k, v in visit_update_dict.items():
                setattr(visit_to_update, k, v)

            await session.commit()

            return visit_to_update
        else:
            return None  
        
    async def delete_visit(self, visit_id: str, session: AsyncSession):
        visit_to_delete = await self.get_visit_by_id(visit_id, session)

        if visit_to_delete is not None:
            await session.delete(visit_to_delete)
            await session.commit()

            return {}
        else:
            return None