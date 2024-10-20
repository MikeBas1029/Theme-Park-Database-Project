from enum import Enum
import sqlalchemy.dialects.mysql as mysql
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

# Importing related models for type-checking
if TYPE_CHECKING:
    from src.models.rides import Rides

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

class RideType(SQLModel, table=True):
    """
    Represents a specific type of ride in the theme park. This model stores the ride type's name, description, and 
    allows for linking to rides of that type. The `RideTypeEnum` is used to ensure consistency in defining ride types.
    """
    __tablename__ = "ride_type"  # Defines the name of the table in the database
    
    # ride_type_id is the primary key for the ride_type table. It uniquely identifies each ride type.
    ride_type_id: int = Field(
        sa_column=Column(mysql.TINYINT, nullable=False, primary_key=True, autoincrement=True, comment="Unique ride type ID"),
        alias="RideTypeID"
    )
    
    # ride_type stores the type of the ride, defined by the RideTypeEnum, ensuring valid values from the enum.
    ride_type: RideTypeEnum = Field(
        sa_column=Column(mysql.VARCHAR(50), unique=True, nullable=False, comment="Type of the ride (based on predefined enums)"),
        alias="RideType"
    )
    
    # description is an optional field that provides a brief description of the ride type.
    description: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(255), comment="Optional description of the ride type"),
        alias="Description"
    )
    
    # Relationships
    # A one-to-many relationship with the Rides model, where one ride type can be associated with many rides.
    rides: List["Rides"] = Relationship(back_populates="ride_type_rel")
    
    # Indexing the `ride_type` field for faster queries based on ride type.
    __table_args__ = (
        Index("idx_ride_type", "ride_type"),
    )