import string 
import secrets
from src.models.emp_auth import EmpAuth 
from sqlmodel.ext.asyncio.session import AsyncSession 
from sqlmodel import select
from src.schemas.emp_auth import EmpAuthCreateModel
from src.utils import generate_hash, verify_password

def generate_username(first_name: str, last_name: str) -> str:
    return first_name[0].lower() + last_name[0].lower() + last_name[1:]

def generate_first_password() -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))


class EmpAuthService:
    async def get_all_employees(self, session: AsyncSession):
        query = select(EmpAuth).order_by(EmpAuth.last_name)

        result = await session.exec(query)

        return result.all()
    
    async def get_user_by_id(self, employee_id: str, session: AsyncSession):
        statement = select(EmpAuth).where(EmpAuth.employee_id == employee_id)

        result = await session.exec(statement)

        user = result.first()

        return user if user is not None else None 
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(EmpAuth).where(EmpAuth.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user if user is not None else None 

    async def user_exists(self, employee_id: str, session: AsyncSession):
        user = await self.get_user_by_id(employee_id, session)

        return bool(user)
    
    async def create_user(self, user_data: EmpAuthCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = EmpAuth(**user_data_dict)

        # update the hash
        first_password = generate_first_password()
        new_user.username = generate_username(new_user.first_name, new_user.last_name)
        new_user.password_on_create = first_password
        new_user.password_hash = generate_hash(first_password)

        session.add(new_user)
    
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
    async def update_user(self, user: EmpAuth, user_data: dict, session: AsyncSession):
        user_to_update = await self.get_user_by_email(EmpAuth.email, session)


        if user_to_update is not None:

            for k, v in user_data.items():
                setattr(user, k, v)

            user_to_update['password_on_create'] = None

            await session.commit()
            return user
        else: 
            return None 
        
    async def delete_user(self, employee_id: str, session: AsyncSession):
        emp_to_delete = await self.get_user_by_id(employee_id, session)

        if emp_to_delete is not None:
            await session.delete(emp_to_delete)
            await session.commit()

            return {}
        else: 
            return None
        