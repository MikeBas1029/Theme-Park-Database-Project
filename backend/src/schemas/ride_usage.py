from datetime import time, date
from pydantic import BaseModel

class RideUsageInputModel(BaseModel):
    customer_id: int 
    ride_id: int 
    usage_date: date 
    queue_time: time 

class RideUsageOutputModel(BaseModel):
    ride_usage_id: int 
    customer_id: int 
    ride_id: int 
    usage_date: date 
    queue_time: time 