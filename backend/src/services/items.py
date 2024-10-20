from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.schemas.items import Item, ItemCreateModel, ItemUpdateModel

class ItemService:

    async def get_all_items(self, session: AsyncSession):
        result = await session.execute(select(Item))
        return result.scalars().all()

    async def get_item_by_sku(self, sku: int, session: AsyncSession):
        return await session.get(Item, sku)

    async def create_item(self, item_data: ItemCreateModel, session: AsyncSession):
        new_item = Item(**item_data.dict())
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        return new_item

    async def update_item(self, sku: int, update_data: ItemUpdateModel, session: AsyncSession):
        item = await session.get(Item, sku)
        if not item:
            return None
        item_data = update_data.dict(exclude_unset=True)
        for key, value in item_data.items():
            setattr(item, key, value)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def delete_item(self, sku: int, session: AsyncSession):
        item = await session.get(Item, sku)
        if not item:
            return None
        await session.delete(item)
        await session.commit()
        return item
