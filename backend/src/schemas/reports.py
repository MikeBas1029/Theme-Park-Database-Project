from pydantic import BaseModel

class MonthlyWeeklyCustomerCount(BaseModel):
    month: int 
    week: int
    num_customers: int