from datetime import date
from typing import Optional
from pydantic import BaseModel
from enum import Enum 

class RideStatus(str, Enum):
    open = "OPEN"
    closed_maint = "CLOSED(M)"
    closed_rainout = "CLOSED(RO)"

class Ride(BaseModel):
    ride_id: int
    section_id: int
    name: str 
    ride_type: int
    last_inspected: date 
    height_requirement: int 
    capacity: int 
    status: RideStatus 

class RideCreateModel(BaseModel):
    section_id: int
    name: str 
    ride_type: int
    height_requirement: int 
    capacity: int 
    status: RideStatus 

class RideUpdateModel(BaseModel):
    section_id: int
    name: str 
    ride_type: Optional[int]
    last_inspected: Optional[date | None] = None
    height_requirement: Optional[int]
    capacity: Optional[int ]
    status: Optional[RideStatus] 