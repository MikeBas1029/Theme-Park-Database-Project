from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.po_details import PurchaseOrderDetails
from src.schemas.po_details import PurchaseOrderDetailsInputModel

class PurchaseOrderDetailsService:
    async def get_all_po_details(self, session: AsyncSession):
        query = select(PurchaseOrderDetails)

        result = await session.exec(query)

        return result.all()
    
    async def get_po_detail_by_id(self, po_detail_id: str, session: AsyncSession):
        query = select(PurchaseOrderDetails).where(PurchaseOrderDetails.order_details_id == po_detail_id)

        result = await session.exec(query)

        po_detail = result.first()

        return po_detail if po_detail is not None else None 
    
    async def po_detail_exists(self, po_detail_id: str, session: AsyncSession):
        query = select(PurchaseOrderDetails).where(PurchaseOrderDetails.order_details_id == po_detail_id)

        result = await session.exec(query)

        po_detail = result.first()

        return bool(po_detail)
    
    async def create_po_detail(
            self,
            po_detail_data: PurchaseOrderDetailsInputModel,
            session: AsyncSession
    ):
        po_detail_data_dict = po_detail_data.model_dump()

        new_po_detail = PurchaseOrderDetails(**po_detail_data_dict)

        # First check if po_detail exists already
        existing_po_detail = await self.po_detail_exists(new_po_detail.order_details_id, session)

        if existing_po_detail:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"PurchaseOrder with po_detail_id {new_po_detail.order_id} already exists.")
        else:
            session.add(new_po_detail)

            await session.commit()

            return new_po_detail
    

    async def update_po_detail(
            self, 
            po_detail_id: str,
            update_data: PurchaseOrderDetailsInputModel,
            session: AsyncSession
    ):
        po_detail_to_update = await self.get_po_detail_by_id(po_detail_id, session)


        if po_detail_to_update is not None:
            po_detail_update_dict = update_data.model_dump()

            for k, v in po_detail_update_dict.items():
                setattr(po_detail_to_update, k, v)

            await session.commit()

            return po_detail_to_update
        else:
            return None  
        
    async def delete_po_detail(self, po_detail_id: str, session: AsyncSession):
        po_detail_to_delete = await self.get_po_detail_by_id(po_detail_id, session)

        if po_detail_to_delete is not None:
            await session.delete(po_detail_to_delete)
            await session.commit()

            return {}
        else:
            return None