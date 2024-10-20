from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Ride(BaseModel):
    ride_id: int
    section_id: int
    name: str 
    ride_type: int
    last_inspected: datetime
    height_requirement: int 
    capacity: int 
    status: str 

class RideCreateModel(BaseModel):
    section_id: int
    name: str 
    ride_type: int
    height_requirement: int 
    capacity: int 
    status: str 

class RideUpdateModel(BaseModel):
    section_id: int
    name: str 
    ride_type: Optional[int]
    last_inspected: Optional[datetime]
    height_requirement: Optional[int]
    capacity: Optional[int ]
    status: Optional[str] 