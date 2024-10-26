from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.work_order_items import WorkOrderItems
from src.schemas.work_order_items import WorkOrderItemInputModel


class WorkOrderItemService:
    async def get_all_work_order_items(self, session: AsyncSession):
        query = select(WorkOrderItems)

        result = await session.exec(query)

        return result.all()
    
    async def get_work_order_item_by_id(self, id: str, session: AsyncSession):
        query = select(WorkOrderItems).where(WorkOrderItems.id == id)

        result = await session.exec(query)

        work_order_item = result.first()

        return work_order_item if work_order_item is not None else None 
    
    async def work_order_item_exists(self, id: str, session: AsyncSession):
        query = select(WorkOrderItems).where(WorkOrderItems.id == id)

        result = await session.exec(query)

        work_order_item = result.first()

        return bool(work_order_item)
    
    async def create_work_order_item(
            self,
            work_order_item_data: WorkOrderItemInputModel,
            session: AsyncSession
    ):
        work_order_item_data_dict = work_order_item_data.model_dump()

        new_work_order_item = WorkOrderItems(**work_order_item_data_dict)

        # First check if work_order_item exists already
        existing_work_order_item = await self.work_order_item_exists(new_work_order_item.id, session)

        if existing_work_order_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"WorkOrderItem with id {new_work_order_item.id} already exists.")
        else:
            session.add(new_work_order_item)

            await session.commit()

            return new_work_order_item
    

    async def update_work_order_item(
            self, 
            id: str,
            update_data: WorkOrderItemInputModel,
            session: AsyncSession
    ):
        work_order_item_to_update = await self.get_work_order_item_by_id(id, session)


        if work_order_item_to_update is not None:
            work_order_item_update_dict = update_data.model_dump()

            for k, v in work_order_item_update_dict.items():
                setattr(work_order_item_to_update, k, v)

            await session.commit()

            return work_order_item_to_update
        else:
            return None  
        
    async def delete_work_order_item(self, id: str, session: AsyncSession):
        work_order_item_to_delete = await self.get_work_order_item_by_id(id, session)

        if work_order_item_to_delete is not None:
            await session.delete(work_order_item_to_delete)
            await session.commit()

            return {}
        else:
            return None