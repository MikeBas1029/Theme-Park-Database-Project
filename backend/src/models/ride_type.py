from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from enum import Enum
from src.models import Rides

class RideTypeEnum(str, Enum):
    ROLLER_COASTER = "roller_coaster"
    FERRIS_WHEEL = "ferris_wheel"
    CAROUSEL = "carousel"
    LOG_FLUME = "log_flume" # water-based rides with log-shaped boats and splash zones
    BUMPER_CARS = "bumper_cars"
    TEACUP_RIDE = "swing_ride" # Rotating cup-shaped cars that spin riders in circles.
    SIMULATOR = "simulator" # Rides that simulate experiences using motion platforms and immersive media.
    DARK_RIDE = "dark_ride" # Indoor rides that often feature special effects and animatronics (e.g., haunted houses).
    WATER_SLIDE = "water_slide"
    ZIPLINE = "zipline"
    FAMILY_RIDES = "family_rides" # Rides suitable for younger children and families, often with gentle motion.

class RideType(SQLModel, table=True):
    __tablename__ = "ride_type"
    
    ride_type_id: int = Field(
        primary_key=True,
        index=True,
        sa_column=Column(mysql.TINYINT, nullable=False, autoincrement=True),  
        alias="RideTypeID"
    )
    ride_type: RideTypeEnum = Field(
        sa_column=Column(mysql.VARCHAR(50), nullable=False, index=True),  
        alias="RideType"
    )
    description: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(255)), alias="Description")  # Optional description

    # Relationships
    rides: List["Rides"] = Relationship(back_populates="ride_type")