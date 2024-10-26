from datetime import datetime
from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.work_orders import WorkOrders
from src.schemas.work_orders import WorkOrderCreateModel, WorkOrderUpdateModel, WorkOrderStatus

class WorkOrderService:
    async def get_all_work_orders(self, session: AsyncSession):
        query = select(WorkOrders).order_by(WorkOrders.date_created)

        result = await session.exec(query)

        return result.all()
    
    async def get_work_order_by_id(self, work_order_id: str, session: AsyncSession):
        query = select(WorkOrders).where(WorkOrders.woid == work_order_id)

        result = await session.exec(query)

        work_order = result.first()

        return work_order if work_order is not None else None 
    
    async def work_order_exists(self, work_order_id: str, session: AsyncSession):
        query = select(WorkOrders).where(WorkOrders.woid == work_order_id)

        result = await session.exec(query)

        work_order = result.first()

        return bool(work_order)
    
    async def create_work_order(
            self,
            work_order_data: WorkOrderCreateModel,
            session: AsyncSession
    ):
        work_order_data_dict = work_order_data.model_dump()

        work_order_data_dict['date_created'] = datetime.now()
        work_order_data_dict['updated_at'] = datetime.now()
        work_order_data_dict['status'] = WorkOrderStatus.IN_PROGRESS.value

        if work_order_data_dict['ride_id'] == '':
            work_order_data_dict['ride_id'] = None

        new_work_order = WorkOrders(**work_order_data_dict)

        # First check if work_order exists already
        existing_work_order = await self.work_order_exists(new_work_order.woid, session)

        if existing_work_order:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"WorkOrder with work_order_id {new_work_order.woid} already exists.")
        else:
            session.add(new_work_order)

            await session.commit()

            return new_work_order
    

    async def update_work_order(
            self, 
            work_order_id: str,
            update_data: WorkOrderUpdateModel,
            session: AsyncSession
    ):
        work_order_to_update = await self.get_work_order_by_id(work_order_id, session)

        if work_order_to_update is not None:
            work_order_update_dict = update_data.model_dump()

            work_order_update_dict['date_created'] = work_order_to_update.date_created
            work_order_update_dict['updated_at'] = datetime.now()


            for k, v in work_order_update_dict.items():
                if k != 'created_on':
                    setattr(work_order_to_update, k, v)


            await session.commit()

            return work_order_to_update
        else:
            return None  
        
    async def delete_work_order(self, work_order_id: str, session: AsyncSession):
        work_order_to_delete = await self.get_work_order_by_id(work_order_id, session)

        if work_order_to_delete is not None:
            await session.delete(work_order_to_delete)
            await session.commit()

            return {}
        else:
            return None