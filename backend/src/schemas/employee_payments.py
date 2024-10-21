from datetime import date 
from pydantic import BaseModel

class EmployeePaymentInputModel(BaseModel):
    employee_id: str
    payment_date: date
    payment_method_id: int

class EmployeePaymentOutputModel(BaseModel):
    employee_payment_id: int
    employee_id: str
    payment_date: date
    payment_method_id: int