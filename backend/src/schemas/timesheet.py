from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel, Field, root_validator, validator
import enum


# Enum representing timesheet status.
class TimesheetStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"


# Base model for timesheet entries.
class TimesheetBaseModel(BaseModel):
    employee_id: str
    section_id: int
    shift_date: date
    punch_in_time: Optional[time]
    punch_out_time: Optional[time]
    meal_break_start: Optional[time] = None
    meal_break_end: Optional[time] = None

    # Validator for parsing time strings to time objects.
    @validator("punch_in_time", "punch_out_time", "meal_break_start", "meal_break_end", pre=True)
    def parse_time(cls, value):
        if isinstance(value, str) and value:
            try:
                return datetime.strptime(value, "%I:%M %p").time()
            except ValueError:
                raise ValueError(f"Invalid time format: {value}. Expected 'HH:MM AM/PM'.")
        elif value == "":
            return None
        return value


# Model for creating new timesheet entries.
class TimesheetCreateModel(TimesheetBaseModel):
    created_by: Optional[str] = None  # Store creator info directly.

    # Set the creator of the timesheet entry.
    @root_validator(pre=True)
    def set_created_by(cls, values):
        if not values.get("created_by"):
            values["created_by"] = values.get("employee_id")  # Default to employee_id if not provided
        return values

    class Config:
        extra = "forbid"  # Disallow extra fields.

# Model for updating existing timesheet entries.
class TimesheetUpdateModel(TimesheetBaseModel):
    status: TimesheetStatus
    updated_by: Optional[str]
    created_on: Optional[str] = Field(exclude=True, default=None)

    class Config:
        extra = "forbid"  # Disallow extra fields.


# Model for outputting timesheet data.
class TimesheetOutputModel(BaseModel):
    shift_id: str
    employee_id: str
    section_id: int
    shift_date: date
    punch_in_time: str
    punch_out_time: str
    meal_break_start: Optional[str]
    meal_break_end: Optional[str]
    status: TimesheetStatus
    created_on: datetime
    updated_on: Optional[datetime]
    created_by: str
    updated_by: Optional[str]

    # Validator for formatting time objects to strings.
    @validator("punch_in_time", "punch_out_time", "meal_break_start", "meal_break_end", pre=True, always=True)
    def format_time(cls, value):
        if isinstance(value, time):
            return value.strftime("%I:%M %p")  # Format to "HH:MM AM/PM"
        return value