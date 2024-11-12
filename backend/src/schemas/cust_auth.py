import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class CustAuth(BaseModel):
    uid: uuid.UUID 
    customer_id: Optional[str | None] = None 
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str 
    is_verified: bool 
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    update_at: datetime 

class CustAuthCreateModel(BaseModel):
    username: str = Field(max_length=14)
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(min_length=8)

class CustAuthLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


