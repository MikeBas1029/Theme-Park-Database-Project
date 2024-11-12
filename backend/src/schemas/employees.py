from enum import Enum
from datetime import date 
from typing import Optional 
from pydantic import BaseModel, EmailStr, Field

class EmployeeType(str, Enum):
    hourly = "Hourly"
    salary = "Salary"

class EmployeeGender(str, Enum):
    male = "M"
    female = "F"
    nonbinary = "N"

class Employee(BaseModel):
    ssn: str
    employee_id: str 
    first_name: str 
    last_name: str 
    middle_initial: Optional[str] 
    phone_number: str 
    email: EmailStr 
    gender: EmployeeGender
    address_line1: str 
    address_line2: Optional[str] 
    city: str 
    state: str
    zip_code: str
    country: str
    dob: date
    start_date: date 
    employee_type: EmployeeType 
    hourly_wage: Optional[float] 
    salary: Optional[float]
    job_function: str 
    department_id: Optional[int | None]


class EmployeeCreateModel(BaseModel):
    ssn: str = Field(max_length=11)
    first_name: str 
    last_name: str 
    middle_initial: Optional[str | None] = None 
    phone_number: str 
    email: EmailStr 
    gender: EmployeeGender
    address_line1: str 
    address_line2: Optional[str | None] = None
    city: str 
    state: str
    zip_code: str
    country: str
    dob: date 
    start_date: date 
    employee_type: EmployeeType 
    hourly_wage: Optional[float] 
    salary: Optional[float]
    job_function: str 
    department_id: Optional[int | None]

class EmployeeUpdateModel(BaseModel):
    ssn: Optional[str] 
    first_name: str 
    last_name: str 
    middle_initial: Optional[str] 
    phone_number: str 
    email: EmailStr 
    gender: Optional[EmployeeGender]
    address_line1: Optional[str] 
    address_line2: Optional[str] 
    city: Optional[str] 
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]
    dob: Optional[date]
    start_date: Optional[date] 
    employee_type: Optional[EmployeeType]
    hourly_wage: Optional[float] 
    salary: Optional[float]
    job_function: Optional[str] 
    department_id: Optional[int | None]

