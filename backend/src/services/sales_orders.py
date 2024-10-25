from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.sales_orders import SalesOrders
from src.schemas.sales_orders import SalesOrdersInputModel


class SalesOrdersService:
    async def get_all_sales_orders(self, session: AsyncSession):
        query = select(SalesOrders).order_by(SalesOrders.order_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_show_by_id(self, show_id: str, session: AsyncSession):
        query = select(SalesOrders).where(SalesOrders.transaction_id == show_id)

        result = await session.exec(query)

        show = result.first()

        return show if show is not None else None 
    
    async def show_exists(self, show_id: str, session: AsyncSession):
        query = select(SalesOrders).where(SalesOrders.transaction_id == show_id)

        result = await session.exec(query)

        show = result.first()

        return bool(show)
    
    async def create_show(
            self,
            show_data: SalesOrdersInputModel,
            session: AsyncSession
    ):
        show_data_dict = show_data.model_dump()

        new_show = SalesOrders(**show_data_dict)

        # First check if show exists already
        existing_show = await self.show_exists(new_show.transaction_id, session)

        if existing_show:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"SalesOrders with show_id {new_show.transaction_id} already exists.")
        else:
            session.add(new_show)

            await session.commit()

            return new_show
    

    async def update_show(
            self, 
            show_id: str,
            update_data: SalesOrdersInputModel,
            session: AsyncSession
    ):
        show_to_update = await self.get_show_by_id(show_id, session)


        if show_to_update is not None:
            show_update_dict = update_data.model_dump()

            for k, v in show_update_dict.items():
                setattr(show_to_update, k, v)

            await session.commit()

            return show_to_update
        else:
            return None  
        
    async def delete_show(self, show_id: str, session: AsyncSession):
        show_to_delete = await self.get_show_by_id(show_id, session)

        if show_to_delete is not None:
            await session.delete(show_to_delete)
            await session.commit()

            return {}
        else:
            return None