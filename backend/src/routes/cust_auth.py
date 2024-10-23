from typing import List
from datetime import timedelta, datetime
from src.db.database import get_session
from fastapi.exceptions import HTTPException 
from fastapi import APIRouter, Depends, status
from src.schemas.cust_auth import CustAuthCreateModel, CustAuth, CustAuthLogin
from src.services.cust_auth import CustAuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse
from src.security import RefreshTokenBearer

cust_auth_router = APIRouter()
cust_auth_service = CustAuthService()
REFRESH_TOKEN_EXPIRY = 2

@cust_auth_router.get("/", response_model=List[CustAuth])
async def get_all_customers(session: AsyncSession = Depends(get_session)):
    customers = await cust_auth_service.get_all_customers(session)
    return customers


@cust_auth_router.get("/{cust_email}", response_model=CustAuth) 
async def get_customer(cust_email: str, session: AsyncSession = Depends(get_session)):
    customer = await cust_auth_service.get_user_by_email(cust_email, session)
    
    if customer:
        return customer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with email {cust_email} not found.") 


@cust_auth_router.post(
    '/signup',
    response_model=CustAuth,
    status_code=status.HTTP_201_CREATED
)
async def signup_user(
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


# @cust_auth_router.delete(
#     "/{cust_email}",
#     status_code=status.HTTP_204_NO_CONTENT
# )
# async def delete_customer(cust_email: str, session: AsyncSession = Depends(get_session)):
#     customer_to_delete = await cust_auth_service.delete_user(cust_email, session)
    
#     if customer_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with email {cust_email} not found.") 

@cust_auth_router.post(
    '/login'
)
async def login_user(login_data: CustAuthLogin, session: AsyncSession = Depends(get_session)):
    email = login_data.email 
    password = login_data.password

    user = await cust_auth_service.get_user_by_email(email, session)

    if user is not None:
        verified = verify_password(password, user.password_hash)

        if verified:
            # create access and refresh token
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "user": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password.")


@cust_auth_router.get('/refresh_token')
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer())
):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )

        return JSONResponse(content={
            "access_token": new_access_token
        })

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token."
        )
