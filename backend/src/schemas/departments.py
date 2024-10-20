from datetime import date 
from typing import Optional 
from pydantic import BaseModel


class Department(BaseModel):
    department_id: int 
    name: str
    manager_id: str
    manager_start_date: date
    num_employees: int
    budget: float
    department_role: Optional[str] 

class DepartmentCreateModel(BaseModel):
    name: str
    manager_id: str
    manager_start_date: date
    num_employees: int
    budget: float
    department_role: Optional[str] 

class DepartmentUpdateModel(BaseModel):
    name: str
    manager_id: Optional[str] 
    manager_start_date: Optional[date]
    num_employees: Optional[int]
    budget: Optional[float]
    department_role: Optional[str] 
