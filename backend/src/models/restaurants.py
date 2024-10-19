from datetime import time
from pydantic import model_validator
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

# Importing related models for type-checking
if TYPE_CHECKING:
    from src.models.sections import Section
    from src.models.employees import Employees

class Restaurants(SQLModel, table=True):
    """
    Represents a restaurant located within a park. This model stores details about the restaurant, 
    including its name, park section, manager, cuisine type, and operating hours.
    """
    __tablename__ = "restaurants"  # Defines the name of the table in the database
    
    # restaurant_id is the primary key for the restaurants table. This uniquely identifies each restaurant.
    restaurant_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique restaurant ID"),
        alias="RestaurantID"
    )
    
    # restaurant_name stores the name of the restaurant and is unique across the table.
    restaurant_name: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, unique=True, comment="Name of the restaurant (unique)"), 
        alias="RestaurantName"
    )
    
    # park_section_id is a foreign key linking to the Sections table. It indicates the section of the park 
    # where the restaurant is located.
    park_section_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("sections.section_id"), nullable=False, index=True, comment="ID of the park section where the restaurant is located"),
        alias="ParkSectionID"
    )
    
    # manager_id is a foreign key linking to the Employees table. It represents the employee who manages 
    # the restaurant.
    manager_id: str = Field(
        sa_column=Column(mysql.VARCHAR(9), ForeignKey("employees.employee_id"), nullable=False, comment="SSN of the employee managing the restaurant"),
        alias="ManagerID"
    )
    
    # cuisine_type represents the type of cuisine the restaurant serves, e.g., Italian, Chinese, etc.
    cuisine_type: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(45), comment="Type of cuisine served by the restaurant"),
        alias="CuisineType"
    )
    
    # opening_time is the time the restaurant opens each day.
    opening_time: time = Field(
        sa_column=Column(mysql.TIME, nullable=False, comment="Opening time of the restaurant"),
        alias="OpeningTime"
    )
    
    # closing_time is the time the restaurant closes each day.
    closing_time: time = Field(
        sa_column=Column(mysql.TIME, nullable=False, comment="Closing time of the restaurant"),
        alias="ClosingTime"
    )
    
    # description is an optional field that gives a brief overview of the restaurant.
    description: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(255), comment="Optional description of the restaurant"),
        alias="Description"
    )
    
    # Relationships
    section: "Section" = Relationship(back_populates="restaurants")  # One-to-many relationship with the Sections table.
    manager: "Employees" = Relationship(back_populates="managed_restaurants")  # One-to-many relationship with the Employees table (manager).
    
    # Validator to ensure that the opening_time is before the closing_time.
    @model_validator(mode='before')
    @classmethod
    def check_times(cls, values):
        """
        Validates that the opening time is before the closing time for the restaurant.
        
        Args:
            cls: The class reference.
            values: The values dictionary containing the fields of the model.
            
        Raises:
            ValueError: If opening time is greater than or equal to closing time.
        
        Returns:
            The validated values dictionary.
        """
        opening_time = values.get("opening_time")
        closing_time = values.get("closing_time")
        
        # Check if opening_time is greater than or equal to closing_time and raise an error if so
        if opening_time and closing_time and opening_time >= closing_time:
            raise ValueError("Opening time must be before closing time.")
        
        return values
    
    __table_args__ = (
        Index("idx_restaurant_id", "restaurant_id"),
        Index("idx_park_section_id", "park_section_id"),
        Index("idx_manager_id", "manager_id"),
    )