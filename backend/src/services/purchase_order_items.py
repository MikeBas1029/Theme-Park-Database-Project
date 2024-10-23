from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.purchase_order_items import PurchaseOrderItems
from src.schemas.purchase_order_items import PurchaseOrderItemInputModel

class PurchaseOrderItemService:
    async def get_all_purchase_order_items(self, session: AsyncSession):
        query = select(PurchaseOrderItems)

        result = await session.exec(query)

        return result.all()
    
    async def get_purchase_order_item_by_id(self, purchase_order_item_id: str, session: AsyncSession):
        query = select(PurchaseOrderItems).where(PurchaseOrderItems.id == purchase_order_item_id)

        result = await session.exec(query)

        purchase_order_item = result.first()

        return purchase_order_item if purchase_order_item is not None else None 
    
    async def purchase_order_item_exists(self, purchase_order_item_id: str, session: AsyncSession):
        query = select(PurchaseOrderItems).where(PurchaseOrderItems.id == purchase_order_item_id)

        result = await session.exec(query)

        purchase_order_item = result.first()

        return bool(purchase_order_item)
    
    async def create_purchase_order_item(
            self,
            purchase_order_item_data: PurchaseOrderItemInputModel,
            session: AsyncSession
    ):
        purchase_order_item_data_dict = purchase_order_item_data.model_dump()

        new_purchase_order_item = PurchaseOrderItems(**purchase_order_item_data_dict)

        # First check if purchase_order_item exists already
        existing_purchase_order_item = await self.purchase_order_item_exists(new_purchase_order_item.id, session)

        if existing_purchase_order_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"PurchaseOrderItem with purchase_order_item_id {new_purchase_order_item.id} already exists.")
        else:
            session.add(new_purchase_order_item)

            await session.commit()

            return new_purchase_order_item
    

    async def update_purchase_order_item(
            self, 
            purchase_order_item_id: str,
            update_data: PurchaseOrderItemInputModel,
            session: AsyncSession
    ):
        purchase_order_item_to_update = await self.get_purchase_order_item_by_id(purchase_order_item_id, session)


        if purchase_order_item_to_update is not None:
            purchase_order_item_update_dict = update_data.model_dump()

            for k, v in purchase_order_item_update_dict.items():
                setattr(purchase_order_item_to_update, k, v)

            await session.commit()

            return purchase_order_item_to_update
        else:
            return None  
        
    async def delete_purchase_order_item(self, purchase_order_item_id: str, session: AsyncSession):
        purchase_order_item_to_delete = await self.get_purchase_order_item_by_id(purchase_order_item_id, session)

        if purchase_order_item_to_delete is not None:
            await session.delete(purchase_order_item_to_delete)
            await session.commit()

            return {}
        else:
            return None