import enum 
from pydantic import BaseModel

# Enum for status
class FacilityStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    UNDER_MAINTENANCE = "Under Maintenance"

class ParkFacilitiesCreateModel(BaseModel):
    facility_id: int
    facility_name: str
    facility_type: str
    location_id: int 

class ParkFacilitiesUpdateModel(BaseModel):
    facility_id: int
    facility_name: str
    facility_type: str
    location_id: int 
    status: FacilityStatus 


class ParkFacilities(BaseModel):
    facility_id: int
    facility_name: str
    facility_type: str
    location_id: int 
    status: FacilityStatus 