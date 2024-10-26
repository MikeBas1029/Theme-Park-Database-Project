import enum
from typing import Optional
from datetime import date, datetime, timezone
from pydantic import BaseModel, root_validator, Field

class MaintenanceType(str, enum.Enum):
    REPAIR = "repair"
    INSPECTION = "inspection"
    UPGRADE = "upgrade"

class WorkOrderStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"

class WorkOrderBaseModel(BaseModel):
    section_id: int
    ride_id: Optional[str]
    invoice_id: Optional[str]
    maintenance_date: date 
    maintenance_type: MaintenanceType 
    assigned_worker_id: str 

class WorkOrderCreateModel(WorkOrderBaseModel):
    created_by: Optional[str] = None 

    # Set the creator of the timesheet entry.
    @root_validator(pre=True)
    def set_created_by(cls, values):
        if not values.get("created_by"):
            values["created_by"] = values.get("assigned_worker_id")  # Default to employee_id if not provided
        return values

    class Config:
        extra = "forbid"  # Disallow extra fields.

class WorkOrderUpdateModel(WorkOrderBaseModel):
    status: WorkOrderStatus 
    updated_by: Optional[str] = Field(exclude=True, default=None)

class WorkOrderOutputModel(BaseModel):
    woid: str
    section_id: int
    ride_id: Optional[str]
    invoice_id: Optional[str]
    maintenance_date: date 
    maintenance_type: MaintenanceType 
    assigned_worker_id: str 
    status: WorkOrderStatus
    created_by: str 
    date_created: datetime 
    updated_by: Optional[str]
    updated_at: Optional[datetime]
