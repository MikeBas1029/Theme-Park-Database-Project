from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.purchase_orders import PurchaseOrders
from src.schemas.purchase_orders import PurchaseOrderCreateModel, PurchaseOrderUpdateModel, OrderStatus

class PurchaseOrderService:
    async def get_all_purchase_orders(self, session: AsyncSession):
        query = select(PurchaseOrders).order_by(PurchaseOrders.order_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_purchase_order_by_id(self, purchase_order_id: str, session: AsyncSession):
        query = select(PurchaseOrders).where(PurchaseOrders.order_id == purchase_order_id)

        result = await session.exec(query)

        purchase_order = result.first()

        return purchase_order if purchase_order is not None else None 
    
    async def purchase_order_exists(self, purchase_order_id: str, session: AsyncSession):
        query = select(PurchaseOrders).where(PurchaseOrders.order_id == purchase_order_id)

        result = await session.exec(query)

        purchase_order = result.first()

        return bool(purchase_order)
    
    async def create_purchase_order(
            self,
            purchase_order_data: PurchaseOrderCreateModel,
            session: AsyncSession
    ):
        purchase_order_data_dict = purchase_order_data.model_dump()

        # Set default status if not provided
        purchase_order_data_dict['order_status'] = OrderStatus.PENDING.value

        new_purchase_order = PurchaseOrders(**purchase_order_data_dict)

        # First check if purchase_order exists already
        existing_purchase_order = await self.purchase_order_exists(new_purchase_order.order_id, session)

        if existing_purchase_order:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"PurchaseOrder with purchase_order_id {new_purchase_order.order_id} already exists.")
        else:
            session.add(new_purchase_order)

            await session.commit()

            return new_purchase_order
    

    async def update_purchase_order(
            self, 
            purchase_order_id: str,
            update_data: PurchaseOrderUpdateModel,
            session: AsyncSession
    ):
        purchase_order_to_update = await self.get_purchase_order_by_id(purchase_order_id, session)


        if purchase_order_to_update is not None:
            purchase_order_update_dict = update_data.model_dump()

            for k, v in purchase_order_update_dict.items():
                setattr(purchase_order_to_update, k, v)

            await session.commit()

            return purchase_order_to_update
        else:
            return None  
        
    async def delete_purchase_order(self, purchase_order_id: str, session: AsyncSession):
        purchase_order_to_delete = await self.get_purchase_order_by_id(purchase_order_id, session)

        if purchase_order_to_delete is not None:
            await session.delete(purchase_order_to_delete)
            await session.commit()

            return {}
        else:
            return None