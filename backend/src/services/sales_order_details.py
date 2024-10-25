from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.sales_order_details import SalesOrderDetail
from src.schemas.sales_order_details import SalesOrderDetailInputModel


class SalesOrderDetailService:
    async def get_all_sales_order_details(self, session: AsyncSession):
        query = select(SalesOrderDetail)

        result = await session.exec(query)

        return result.all()
    
    async def get_so_detail_by_id(self, detail_id: str, session: AsyncSession):
        query = select(SalesOrderDetail).where(SalesOrderDetail.detail_id == detail_id)

        result = await session.exec(query)

        detail = result.first()

        return detail if detail is not None else None 
    
    async def so_detail_exists(self, detail_id: str, session: AsyncSession):
        query = select(SalesOrderDetail).where(SalesOrderDetail.detail_id == detail_id)

        result = await session.exec(query)

        detail = result.first()

        return bool(detail)
    
    async def create_so_detail(
            self,
            detail_data: SalesOrderDetailInputModel,
            session: AsyncSession
    ):
        detail_data_dict = detail_data.model_dump()

        new_detail = SalesOrderDetail(**detail_data_dict)

        # First check if detail exists already
        existing_detail = await self.so_detail_exists(new_detail.detail_id, session)

        if existing_detail:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"SalesOrderDetail with detail_id {new_detail.detail_id} already exists.")
        else:
            session.add(new_detail)

            await session.commit()

            return new_detail
    

    async def update_so_detail(
            self, 
            detail_id: str,
            update_data: SalesOrderDetailInputModel,
            session: AsyncSession
    ):
        detail_to_update = await self.get_so_detail_by_id(detail_id, session)


        if detail_to_update is not None:
            detail_update_dict = update_data.model_dump()

            for k, v in detail_update_dict.items():
                setattr(detail_to_update, k, v)

            await session.commit()

            return detail_to_update
        else:
            return None  
        
    async def delete_so_detail(self, detail_id: str, session: AsyncSession):
        detail_to_delete = await self.get_so_detail_by_id(detail_id, session)

        if detail_to_delete is not None:
            await session.delete(detail_to_delete)
            await session.commit()

            return {}
        else:
            return None