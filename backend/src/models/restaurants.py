from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import time
from pydantic import root_validator
from src.models import Section, Employees

class Restaurants(SQLModel, table=True):
    __tablename__ = "restaurants"
    
    restaurant_id: int = Field(
        primary_key=True,
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="RestaurantID"
    )
    restaurant_name: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, unique=True),  # Unique constraint
        alias="RestaurantName"
    )
    park_section_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False, index=True),  # Added index
        foreign_key="sections.SectionID",
        alias="ParkSectionID"
    )
    manager_id: Optional[int] = Field(
        sa_column=Column(mysql.INTEGER, index=True),  # Added index
        foreign_key="employees.SSN",
        alias="ManagerID"
    )
    cuisine_type: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(45)), alias="CuisineType")
    opening_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="OpeningTime")
    closing_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="ClosingTime")
    description: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(255)), alias="Description")  # Optional description

    # Relationships
    section: "Section" = Relationship(back_populates="restaurants")
    manager: Optional["Employees"] = Relationship(back_populates="managed_restaurants")
    
    @root_validator
    def check_times(cls, values):
        opening_time = values.get("opening_time")
        closing_time = values.get("closing_time")
        if opening_time and closing_time and opening_time >= closing_time:
            raise ValueError("Opening time must be before closing time.")
        return values