from datetime import time, datetime
from typing import Optional
from pydantic import BaseModel, validator


class RestaurantInputModel(BaseModel):
    restaurant_name: str
    park_section_id: int
    manager_id: str 
    cuisine_type: Optional[str | None] = None
    opening_time: time 
    closing_time: time 
    description: Optional[str | None] = None

    @validator("opening_time", pre=True)
    def parse_opening_time(cls, value):
        # Handle input in "HH:MM" format
        if isinstance(value, str):
            try:
                # Parse "HH:MM" format and set seconds and microseconds to zero
                parsed_time = datetime.strptime(value, "%I:%M %p").time()
                return parsed_time
            except ValueError:
                raise ValueError(f"Invalid time format: {value}. Expected format is 'HH:MM AM/PM'.")
        return value

    @validator("closing_time", pre=True)
    def parse_closing_time(cls, value):
        # Handle input in "HH:MM" format
        if isinstance(value, str):
            try:
                # Parse "HH:MM" format and set seconds and microseconds to zero
                parsed_time = datetime.strptime(value, "%I:%M %p").time()
                return parsed_time
            except ValueError:
                raise ValueError(f"Invalid time format: {value}. Expected format is 'HH:MM AM/PM'.")
        return value


class RestaurantOutputModel(BaseModel):
    restaurant_id: str 
    restaurant_name: str
    park_section_id: int
    manager_id: str 
    cuisine_type: str
    opening_time: str 
    closing_time: str 
    description: str

    @validator("opening_time", pre=True, always=True)
    def format_opening_time(cls, value):
        if isinstance(value, time):
            return value.strftime("%I:%M %p")  # Format to "HH:MM"
        return value

    @validator("closing_time", pre=True, always=True)
    def format_closing_time(cls, value):
        if isinstance(value, time):
            return value.strftime("%I:%M %p")  # Format to "HH:MM"
        return value