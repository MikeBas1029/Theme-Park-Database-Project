from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.rentals import Rentals
from src.schemas.rentals import RentalsInputModel


class RentalsService:
    async def get_all_rentals(self, session: AsyncSession):
        query = select(Rentals).order_by(Rentals.rental_type)

        result = await session.exec(query)

        return result.all()
    
    async def get_rental_by_id(self, rental_id: str, session: AsyncSession):
        query = select(Rentals).where(Rentals.rental_id == rental_id)

        result = await session.exec(query)

        rental = result.first()

        return rental if rental is not None else None 
    
    async def rental_exists(self, rental_id: str, session: AsyncSession):
        query = select(Rentals).where(Rentals.rental_id == rental_id)

        result = await session.exec(query)

        rental = result.first()

        return bool(rental)
    
    async def create_rental(
            self,
            rental_data: RentalsInputModel,
            session: AsyncSession
    ):
        rental_data_dict = rental_data.model_dump()

        new_rental = Rentals(**rental_data_dict)

        # First check if rental exists already
        existing_rental = await self.rental_exists(new_rental.rental_id, session)

        if existing_rental:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Rentals with rental_id {new_rental.rental_id} already exists.")
        else:
            session.add(new_rental)

            await session.commit()

            return new_rental
    

    async def update_rental(
            self, 
            rental_id: str,
            update_data: RentalsInputModel,
            session: AsyncSession
    ):
        rental_to_update = await self.get_rental_by_id(rental_id, session)


        if rental_to_update is not None:
            rental_update_dict = update_data.model_dump()

            for k, v in rental_update_dict.items():
                setattr(rental_to_update, k, v)

            await session.commit()

            return rental_to_update
        else:
            return None  
        
    async def delete_rental(self, rental_id: str, session: AsyncSession):
        rental_to_delete = await self.get_rental_by_id(rental_id, session)

        if rental_to_delete is not None:
            await session.delete(rental_to_delete)
            await session.commit()

            return {}
        else:
            return None