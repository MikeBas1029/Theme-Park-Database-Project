from typing import List
from datetime import timedelta, datetime
from src.db.database import get_session
from fastapi.exceptions import HTTPException 
from fastapi import APIRouter, Depends, status
from src.schemas.emp_auth import EmpAuthCreateModel, EmpAuth, EmpAuthLogin
from src.services.emp_auth import EmpAuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse
from src.security import RefreshTokenBearer

emp_auth_router = APIRouter()
emp_auth_service = EmpAuthService()
REFRESH_TOKEN_EXPIRY = 2

@emp_auth_router.get("/", response_model=List[EmpAuth])
async def get_all_employees(session: AsyncSession = Depends(get_session)):
    employees = await emp_auth_service.get_all_employees(session)
    return employees


@emp_auth_router.get("/{employee_id}", response_model=EmpAuth) 
async def get_employee(employee_id: str, session: AsyncSession = Depends(get_session)):
    employee = await emp_auth_service.get_user_by_id(employee_id, session)
    
    if employee:
        return employee
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Empomer with ID {employee_id} not found.") 


@emp_auth_router.post(
    '/signup',
    response_model=EmpAuth,
    status_code=status.HTTP_201_CREATED
)
async def signup_user(
    user_data: EmpAuthCreateModel,
    session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await emp_auth_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User with email already exists."
        )
    
    new_user = await emp_auth_service.create_user(user_data, session)

    return new_user


@emp_auth_router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee(employee_id: str, session: AsyncSession = Depends(get_session)):
    employee_to_delete = await emp_auth_service.delete_user(employee_id, session)
    
    if employee_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {employee_id} not found.") 

@emp_auth_router.post(
    '/login'
)
async def login_user(login_data: EmpAuthLogin, session: AsyncSession = Depends(get_session)):
    email = login_data.email 
    password = login_data.password

    user = await emp_auth_service.get_user_by_email(email, session)

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


@emp_auth_router.get('/refresh_token')
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
