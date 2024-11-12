from datetime import date 
from typing import Optional 
from pydantic import BaseModel


class Department(BaseModel):
    department_id: int 
    name: str
    num_employees: int
    budget: float
    department_role: Optional[str] 

class DepartmentCreateModel(BaseModel):
    name: str
    num_employees: int
    budget: float
    department_role: Optional[str] 

class DepartmentUpdateModel(BaseModel):
    name: str
    num_employees: Optional[int]
    budget: Optional[float]
    department_role: Optional[str] 
