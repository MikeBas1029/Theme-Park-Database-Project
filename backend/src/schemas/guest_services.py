from datetime import date 
from typing import Optional
from pydantic import BaseModel

class GuestServiceInputModel(BaseModel):
    customer_id: str 
    request_type: str
    description: str
    service_date: date
    employee_id: Optional[str | None] = None 

class GuestServiceOutputModel(BaseModel):
    service_request_id: str 
    customer_id: str 
    request_type: str
    description: str
    service_date: date
    employee_id: str