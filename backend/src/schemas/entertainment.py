from datetime import date, datetime, time
from pydantic import BaseModel, validator
import enum

class ShowStatus(str, enum.Enum):
    active = "Active"
    canceled = "Canceled"
    postponed = "Postponed"
    discontinued = "Discontinued"

class EntertainmentInputModel(BaseModel):
    section_id: int
    show_name: str
    show_date: date
    show_time: time # Expects input in HH:MM AM/PM format
    capacity: int
    ticket_price: float
    status: ShowStatus

    @validator("show_time", pre=True)
    def parse_show_time(cls, value):
        # Handle input in "HH:MM" format
        if isinstance(value, str):
            try:
                # Parse "HH:MM" format and set seconds and microseconds to zero
                parsed_time = datetime.strptime(value, "%I:%M %p").time()
                return parsed_time
            except ValueError:
                raise ValueError(f"Invalid time format: {value}. Expected format is 'HH:MM'.")
        return value

class EntertainmentOutputModel(BaseModel):
    show_id: str
    section_id: int
    show_name: str
    show_date: date
    show_time: str  
    capacity: int
    ticket_price: float
    status: ShowStatus

    @validator("show_time", pre=True, always=True)
    def format_show_time(cls, value):
        if isinstance(value, time):
            return value.strftime("%I:%M %p")  # Format to "HH:MM"
        return value