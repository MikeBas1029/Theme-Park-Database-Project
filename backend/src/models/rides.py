from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import datetime
from typing import Optional, List
from src.models import RideType, WorkOrders, Section, RideUsage

class Rides(SQLModel, table=True):
    __tablename__ = "rides"
    
    ride_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="RideID"
    )
    section_id: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="sections.SectionID",
        alias="SectionID"
    )
    name: str = Field(
        default=None,
        sa_column=Column(mysql.VARCHAR(50), nullable=False),
        alias="Name"
    )
    ride_type: int = Field(
        default=None,
        sa_column=Column(mysql.TINYINT(), nullable=False),
        foreign_key="ride_type.ride_type_id",  
        alias="RideType"
    )
    last_inspected: datetime = Field(
        default=None,
        sa_column=Column(mysql.TIMESTAMP(), nullable=False),
        alias="LastInspected"
    )
    woid: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="workorder.WOID",
        alias="WOID"
    )
    height_requirement: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, nullable=False, comment="Height required to go on the ride."),
        alias="HeightRequirement"
    )
    capacity: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="Capacity"
    )
    status: str = Field(
        default=None,  
        sa_column=Column(mysql.ENUM("OPEN", "CLOSED - MAINTENANCE", "CLOSED - RAINOUT"), nullable=False, comment="The state of the ride: OPEN, CLOSED - Maintenance, CLOSED - RainOut."),
        alias="Status"
    )
    
    # Relationships
    ride_type: "RideType" = Relationship(back_populates="rides")
    work_order: "WorkOrders" = Relationship(back_populates="rides")
    section: "Section" = Relationship(back_populates="rides")
    ride_usages: List["RideUsage"] = Relationship(back_populates="ride")
