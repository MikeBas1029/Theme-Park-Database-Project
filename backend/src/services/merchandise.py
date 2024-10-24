from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.merchandise import Merchandise
from src.schemas.merchandise import MerchandiseInputModel


class MerchandiseService:
    async def get_all_merchandise(self, session: AsyncSession):
        query = select(Merchandise)

        result = await session.exec(query)

        return result.all()
    
    async def get_merchandise_by_id(self, merchandise_id: str, session: AsyncSession):
        query = select(Merchandise).where(Merchandise.merchandise_id == merchandise_id)

        result = await session.exec(query)

        merchandise = result.first()

        return merchandise if merchandise is not None else None 
    
    async def merchandise_exists(self, merchandise_id: str, session: AsyncSession):
        query = select(Merchandise).where(Merchandise.merchandise_id == merchandise_id)

        result = await session.exec(query)

        merchandise = result.first()

        return bool(merchandise)
    
    async def create_merchandise(
            self,
            merchandise_data: MerchandiseInputModel,
            session: AsyncSession
    ):
        merchandise_data_dict = merchandise_data.model_dump()

        new_merchandise = Merchandise(**merchandise_data_dict)

        # First check if merchandise exists already
        existing_merchandise = await self.merchandise_exists(new_merchandise.merchandise_id, session)

        if existing_merchandise:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Merchandise with merchandise_id {new_merchandise.merchandise_id} already exists.")
        else:
            session.add(new_merchandise)

            await session.commit()

            return new_merchandise
    

    async def update_merchandise(
            self, 
            merchandise_id: str,
            update_data: MerchandiseInputModel,
            session: AsyncSession
    ):
        merchandise_to_update = await self.get_merchandise_by_id(merchandise_id, session)


        if merchandise_to_update is not None:
            merchandise_update_dict = update_data.model_dump()

            for k, v in merchandise_update_dict.items():
                setattr(merchandise_to_update, k, v)

            await session.commit()

            return merchandise_to_update
        else:
            return None  
        
    async def delete_merchandise(self, merchandise_id: str, session: AsyncSession):
        merchandise_to_delete = await self.get_merchandise_by_id(merchandise_id, session)

        if merchandise_to_delete is not None:
            await session.delete(merchandise_to_delete)
            await session.commit()

            return {}
        else:
            return None