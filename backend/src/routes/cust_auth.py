from typing import List
from src.db.database import get_session
from fastapi.exceptions import HTTPException 
from fastapi import APIRouter, Depends, status
from src.schemas.cust_auth import CustAuthCreateModel, CustAuth
from src.services.cust_auth import CustAuthService
from sqlmodel.ext.asyncio.session import AsyncSession

cust_auth_router = APIRouter()
cust_auth_service = CustAuthService()

@cust_auth_router.get("/", response_model=List[CustAuth])
async def get_all_customers(session: AsyncSession = Depends(get_session)):
    customers = await cust_auth_service.get_all_customers(session)
    return customers


@cust_auth_router.get("/{cust_email}", response_model=CustAuth) 
async def get_customer(cust_email: str, session: AsyncSession = Depends(get_session)):
    customer = await cust_auth_service.get_customer_by_email(cust_email, session)
    
    if customer:
        return customer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with email {cust_email} not found.") 


@cust_auth_router.post(
    '/signup',
    response_model=CustAuth,
    status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: CustAuthCreateModel,
    session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await cust_auth_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User with email already exists."
        )
    
    new_user = await cust_auth_service.create_user(user_data, session)

    return new_user


@cust_auth_router.delete(
    "/{cust_email}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_customer(cust_email: str, session: AsyncSession = Depends(get_session)):
    customer_to_delete = await cust_auth_service.delete_user(cust_email, session)
    
    if customer_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with email {cust_email} not found.") 

