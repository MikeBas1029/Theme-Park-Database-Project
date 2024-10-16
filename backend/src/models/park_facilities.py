from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Section

# Enum for status
class FacilityStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    UNDER_MAINTENANCE = "Under Maintenance"

class ParkFacilities(SQLModel, table=True):
    __tablename__ = "parkfacilities"
    
    facility_id: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="FacilityID"
    )
    facility_name: str = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False), index=True, alias="FacilityName")  # Adjust length based on need
    facility_type: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="FacilityType")  # Adjust length
    location_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),  
        foreign_key="sections.SectionID",
        alias="LocationID"
    )
    status: FacilityStatus = Field(sa_column=Column(mysql.ENUM(FacilityStatus), nullable=False), alias="Status")

    # Relationships
    section: "Section" = Relationship(back_populates="facilities", cascade_delete=True)  # Ensure cascading deletes if needed

   