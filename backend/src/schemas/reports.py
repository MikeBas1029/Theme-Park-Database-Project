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

class InvoiceStatus(BaseModel):
    invoice_id: str 
    company_name: str 
    supply: str
    amount_due: float 
    payment_status: str

class HoursWorked(BaseModel):
    first_name: str 
    last_name: str 
    job_function: str 
    department: str 
    year: int 
    month: str 
    day: str 
    hours_worked: int 