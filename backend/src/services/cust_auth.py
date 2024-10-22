from src.models.cust_auth import CustAuth 
from sqlmodel.ext.asyncio.session import AsyncSession 
from sqlmodel import select
from src.schemas.cust_auth import CustAuthCreateModel
from src.utils import generate_hash, verify_password

class CustAuthService:
    async def get_all_customers(self, session: AsyncSession):
        query = select(CustAuth).order_by(CustAuth.last_name)

        result = await session.exec(query)

        return result.all()
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(CustAuth).where(CustAuth.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user if user is not None else None 

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return bool(user)
    
    async def create_user(self, user_data: CustAuthCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = CustAuth(**user_data_dict)

        # update the hash
        new_user.password_hash = generate_hash(user_data_dict['password'])

        session.add(new_user)
    
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
    async def update_user(self, user: CustAuth, user_data: dict, session: AsyncSession):
        user_to_update = await self.get_user_by_email(CustAuth.email, session)

        if user_to_update is not None:

            for k, v in user_data.items():
                setattr(user, k, v)

            await session.commit()
            return user
        else: 
            return None 
        
    async def delete_user(self, email: str, session: AsyncSession):
        cust_to_delete = await self.get_user_by_email(email, session)

        if cust_to_delete is not None:
            await session.delete(cust_to_delete)
            await session.commit()

            return {}
        else: 
            return None
        