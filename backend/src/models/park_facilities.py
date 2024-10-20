import enum 
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import Enum as SAEnum

if TYPE_CHECKING:
    from src.models.sections import Section

# Enum for status
class FacilityStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    UNDER_MAINTENANCE = "Under Maintenance"

class ParkFacilities(SQLModel, table=True):
    __tablename__ = "parkfacilities"
    
    # facility_id is the primary key for the ParkFacilities table, uniquely identifying each facility.
    facility_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique ID for each facility"),
        alias="FacilityID"
    )
    
    # facility_name is the name of the facility (e.g., "Restroom", "First Aid").
    facility_name: str = Field(
        sa_column=Column(mysql.VARCHAR(100), nullable=False, index=True, comment="Name of the facility"), 
        alias="FacilityName"
    )
    
    # facility_type represents the type of the facility (e.g., "Restroom", "Food Court").
    facility_type: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, comment="Type of the facility"), 
        alias="FacilityType"
    )
    
    # location_id is a foreign key linking to the Section table, indicating where the facility is located.
    location_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("sections.section_id"), nullable=False, comment="Foreign key referencing SectionID in Sections table"),  
        alias="LocationID"
    )
    
    # status is an Enum that stores the status of the facility (e.g., "Active", "Inactive", "Under Maintenance").
    status: FacilityStatus = Field(
        sa_column=Column(
            SAEnum(FacilityStatus, values_callable=lambda x: [e.value for e in x]), 
            nullable=False, 
            comment="Status of the facility"), 
        alias="Status"
    )

    # Relationships
    # The facility is associated with a section, defined by the foreign key to the Section table.
    section: "Section" = Relationship(back_populates="facilities")  # Ensures cascading deletes if the section is deleted

    # Table index: Adds an index to improve query performance on facility_id.
    __table_args__ = (
        Index("idx_facility_id", "facility_id"),
    )