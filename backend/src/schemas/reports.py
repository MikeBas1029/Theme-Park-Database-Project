from pydantic import BaseModel

class MonthlyWeeklyCustomerCount(BaseModel):
    month: int 
    week: int
    num_customers: int

class FrequentRide(BaseModel):
    month: int 
    name: str
    num_rides: int