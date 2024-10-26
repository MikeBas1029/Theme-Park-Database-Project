import uuid 
import enum
from typing import Optional
from datetime import datetime
from pydantic import EmailStr, BaseModel, Field

class EmpRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class EmpAuth(BaseModel):
    uid: uuid.UUID 
    employee_id: Optional[str] 
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: EmpRole 
    is_verified: bool 
    password_on_create: Optional[str] 
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    update_at: datetime 

class EmpAuthCreateModel(BaseModel):
    employee_id: str 
    email: EmailStr
    first_name: str
    last_name: str
    role: EmpRole = EmpRole.employee

class EmpAuthLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)