from datetime import time, datetime
from pydantic import BaseModel, validator

class ShopInputModel(BaseModel):
    shop_name: str
    address: str
    park_section_id: int 
    manager_id: str 
    opening_time: time
    closing_time: time


    @validator("opening_time", pre=True)
    def parse_shop_opening_time(cls, value):
        # Handle input in "HH:MM" format
        if isinstance(value, str):
            try:
                # Parse "HH:MM" format and set seconds and microseconds to zero
                parsed_time = datetime.strptime(value, "%I:%M %p").time()
                return parsed_time
            except ValueError:
                raise ValueError(f"Invalid time format: {value}. Expected format is 'HH:MM'.")
        return value

    @validator("closing_time", pre=True)
    def parse_shop_closing_time(cls, value):
        # Handle input in "HH:MM" format
        if isinstance(value, str):
            try:
                # Parse "HH:MM" format and set seconds and microseconds to zero
                parsed_time = datetime.strptime(value, "%I:%M %p").time()
                return parsed_time
            except ValueError:
                raise ValueError(f"Invalid time format: {value}. Expected format is 'HH:MM'.")
        return value


class ShopOutputModel(BaseModel):
    shop_id: str 
    shop_name: str
    address: str
    park_section_id: int 
    manager_id: str 
    opening_time: str
    closing_time: str

    @validator("opening_time", pre=True, always=True)
    def format_shop_opening_time(cls, value):
        if isinstance(value, time):
            return value.strftime("%I:%M %p")  # Format to "HH:MM"
        return value

    @validator("closing_time", pre=True, always=True)
    def format_shop_closing_time(cls, value):
        if isinstance(value, time):
            return value.strftime("%I:%M %p")  # Format to "HH:MM"
        return value