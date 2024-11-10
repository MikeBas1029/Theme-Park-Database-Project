from pydantic import BaseModel
from datetime import date 

class DepartmentManagersModel(BaseModel):
    department_id: int 
    employee_id: str 
    manager_start_date: date

