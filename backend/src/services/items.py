from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.items import Items 
from src.schemas.items import ItemCreateModel, ItemUpdateModel

class ItemService:
    async def get_all_items(self, session: AsyncSession):
        query = select(Items).order_by(Items.name)

        result = await session.exec(query)

        return result.all()
    
    async def get_item_by_sku(self, item_sku: str, session: AsyncSession):
        query = select(Items).where(Items.sku == item_sku)

        result = await session.exec(query)

        item = result.first()

        return item if item is not None else None 
    
    async def item_exists(self, item_sku: str, session: AsyncSession):
        query = select(Items).where(Items.sku == item_sku)

        result = await session.exec(query)

        item = result.first()

        return bool(item)
    
    async def create_item(
            self,
            item_data: ItemCreateModel,
            session: AsyncSession
    ):
        item_data_dict = item_data.model_dump()

        new_item = Items(**item_data_dict)

        # First check if item exists already
        existing_item = await self.item_exists(new_item.sku, session)

        if existing_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Customer with sku {new_item.sku} already exists.")
        else:
            session.add(new_item)

            await session.commit()

            return new_item
    

    async def update_item(
            self, 
            item_sku: str,
            update_data: ItemUpdateModel,
            session: AsyncSession
    ):
        item_to_update = await self.get_item_by_sku(item_sku, session)


        if item_to_update is not None:
            item_update_dict = update_data.model_dump()

            for k, v in item_update_dict.items():
                setattr(item_to_update, k, v)

            await session.commit()

            return item_to_update
        else:
            return None  
        
    async def delete_item(self, item_sku: str, session: AsyncSession):
        item_to_delete = await self.get_item_by_sku(item_sku, session)

        if item_to_delete is not None:
            await session.delete(item_to_delete)
            await session.commit()

            return {}
        else:
            return None