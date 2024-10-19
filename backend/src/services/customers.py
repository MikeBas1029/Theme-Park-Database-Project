from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.customers import Customers 
from src.schemas.customers import CustomerCreateModel, CustomerUpdateModel

class CustomerService:
    async def get_all_customers(self, session: AsyncSession):
        query = select(Customers).order_by(Customers.last_name)

        result = await session.exec(query)

        return result.all()
    
    async def get_customer_by_email(self, cust_email: str, session: AsyncSession):
        query = select(Customers).where(Customers.email == cust_email)

        result = await session.exec(query)

        customer = result.first()

        return customer if customer is not None else None 
    
    async def customer_exists(self, cust_email: str, session: AsyncSession):
        query = select(Customers).where(Customers.email == cust_email)

        result = await session.exec(query)

        customer = result.first()

        return bool(customer)
    
    async def create_customer(
            self,
            cust_data: CustomerCreateModel,
            session: AsyncSession
    ):
        cust_data_dict = cust_data.model_dump()

        new_cust = Customers(**cust_data_dict)

        # First check if customer exists already
        existing_customer = await self.customer_exists(new_cust.email, session)

        if existing_customer:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Customer with email {new_cust.email} already exists.")
        else:
            session.add(new_cust)

            await session.commit()

            return new_cust
    

    async def update_cust(
            self, 
            cust_email: str,
            update_data: CustomerUpdateModel,
            session: AsyncSession
    ):
        cust_to_update = await self.get_customer_by_email(cust_email, session)


        if cust_to_update is not None:
            cust_update_dict = update_data.model_dump()

            for k, v in cust_update_dict.items():
                setattr(cust_to_update, k, v)

            await session.commit()

            return cust_to_update
        else:
            return None  
        
    async def delete_cust(self, cust_email: str, session: AsyncSession):
        cust_to_delete = await self.get_customer_by_email(cust_email, session)

        if cust_to_delete is not None:
            await session.delete(cust_to_delete)
            await session.commit()

            return {}
        else:
            return None