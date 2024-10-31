from pydantic import BaseModel

class MonthlyWeeklyCustomerCount(BaseModel):
    month: int 
    week: int
    num_customers: int

class FrequentRide(BaseModel):
    month: int 
    name: str
    num_rides: int

class BrokenRide(BaseModel):
    Maintenance_Month: int 
    Num_Rides_Maintained: int  # Count of rides
    avg_rides_needing_maint: float 