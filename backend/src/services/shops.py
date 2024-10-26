from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.shops import Shops
from src.schemas.shops import ShopInputModel


class ShopService:
    async def get_all_shops(self, session: AsyncSession):
        query = select(Shops).order_by(Shops.shop_name)

        result = await session.exec(query)

        return result.all()
    
    async def get_shop_by_id(self, shop_id: str, session: AsyncSession):
        query = select(Shops).where(Shops.shop_id == shop_id)

        result = await session.exec(query)

        shop = result.first()

        return shop if shop is not None else None 
    
    async def shop_exists(self, shop_id: str, session: AsyncSession):
        query = select(Shops).where(Shops.shop_id == shop_id)

        result = await session.exec(query)

        shop = result.first()

        return bool(shop)
    
    async def create_shop(
            self,
            shop_data: ShopInputModel,
            session: AsyncSession
    ):
        shop_data_dict = shop_data.model_dump()

        new_shop = Shops(**shop_data_dict)

        # First check if shop exists already
        existing_shop = await self.shop_exists(new_shop.shop_id, session)

        if existing_shop:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Shop with shop_id {new_shop.shop_id} already exists.")
        else:
            session.add(new_shop)

            await session.commit()

            return new_shop
    

    async def update_shop(
            self, 
            shop_id: str,
            update_data: ShopInputModel,
            session: AsyncSession
    ):
        shop_to_update = await self.get_shop_by_id(shop_id, session)


        if shop_to_update is not None:
            shop_update_dict = update_data.model_dump()

            for k, v in shop_update_dict.items():
                setattr(shop_to_update, k, v)

            await session.commit()

            return shop_to_update
        else:
            return None  
        
    async def delete_shop(self, shop_id: str, session: AsyncSession):
        shop_to_delete = await self.get_shop_by_id(shop_id, session)

        if shop_to_delete is not None:
            await session.delete(shop_to_delete)
            await session.commit()

            return {}
        else:
            return None