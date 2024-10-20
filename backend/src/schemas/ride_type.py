from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class RideTypeEnum(str, Enum):
    """
    Enum representing different types of rides in the theme park.
    Each type corresponds to a category of rides, which helps in organizing and querying rides based on their type.
    """
    ROLLER_COASTER = "roller_coaster"
    FERRIS_WHEEL = "ferris_wheel"
    CAROUSEL = "carousel"
    LOG_FLUME = "log_flume"  # Water-based rides with log-shaped boats and splash zones
    BUMPER_CARS = "bumper_cars"
    TEACUP_RIDE = "swing_ride"  # Rotating cup-shaped cars that spin riders in circles.
    SIMULATOR = "simulator"  # Rides that simulate experiences using motion platforms and immersive media.
    DARK_RIDE = "dark_ride"  # Indoor rides that often feature special effects and animatronics (e.g., haunted houses).
    WATER_SLIDE = "water_slide"
    ZIPLINE = "zipline"
    FAMILY_RIDES = "family_rides"  # Rides suitable for younger children and families, often with gentle motion.

class RideTypeInputModel(BaseModel):
    ride_type: RideTypeEnum 
    description: Optional[str] 

class RideTypeOutputModel(BaseModel):
    ride_type_id: int
    ride_type: RideTypeEnum 
    description: str 