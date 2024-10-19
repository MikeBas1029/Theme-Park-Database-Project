from typing import List 
from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.customers import CustomerService
from src.schemas.customers import Customer, CustomerCreateModel, CustomerUpdateModel

customer_router = APIRouter()
customer_service = CustomerService()

@customer_router.get("/", response_model=List[Customer])
async def get_all_customers(session: AsyncSession = Depends(get_session)):
    customers = await customer_service.get_all_customers(session)
    return customers


@customer_router.get("/{cust_email}", response_model=Customer) 
async def get_customer(cust_email: str, session: AsyncSession = Depends(get_session)):
    customer = await customer_service.get_customer_by_email(cust_email, session)
    
    if customer:
        return customer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with email {cust_email} not found.") 



@customer_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Customer,
)
async def create_a_customer(
    cust_data: CustomerCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await customer_service.create_customer(cust_data, session)
    except Exception as error:
        raise error



@customer_router.patch("/{cust_email}", response_model=Customer)
async def update_customer(
    cust_email: str,
    update_data: CustomerUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_customer = await customer_service.update_cust(cust_email, update_data, session)

    if updated_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with email {cust_email} not found.") 
    else:
        return updated_customer


@customer_router.delete(
    "/{cust_email}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_customer(cust_email: str, session: AsyncSession = Depends(get_session)):
    customer_to_delete = await customer_service.delete_cust(cust_email, session)
    
    if customer_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with email {cust_email} not found.") 
