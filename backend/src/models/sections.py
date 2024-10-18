from typing import List, TYPE_CHECKING
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

if TYPE_CHECKING:
    from src.models.departments import Departments
    from src.models.rides import Rides
    from src.models.shops import Shops
    from src.models.restaurants import Restaurants
    from src.models.entertainment import Entertainment

class Section(SQLModel, table=True):
    """
    Represents a section in the theme park, associated with a department and containing various attractions.
    
    Attributes:
        section_id (int): Unique identifier for the section (Primary Key).
        department_id (int): Foreign key linking to the department that owns the section.
        location (str): Location or area of the section within the park.
        name (str): Name of the section (e.g., "Adventure Zone").
        lot_size (str): Size of the section's lot or land area.
    
    Relationships:
        department (Departments): The department that manages this section.
        rides (List[Rides]): List of rides located in this section.
        shops (List[Shops]): List of shops in this section.
        restaurants (List[Restaurants]): List of restaurants in this section.
        entertainment (List[Entertainment]): List of entertainment activities in this section.
    """
    
    __tablename__ = "sections"
    
    # Primary key for the section
    section_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False),
        alias="SectionID"
    )

    # Foreign key linking to the department
    department_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("departments.department_id"),  # Links to the Departments table
            nullable=False
        ),
        alias="DepartmentID"
    )
    
    # Location of the section within the park
    location: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False),
        alias="Location"
    )
    
    # Name of the section
    name: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False),
        alias="Name"
    )
    
    # Size of the section's lot or land area
    lot_size: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False),
        alias="LotSize"
    )

    # Relationships with other models
    department: "Departments" = Relationship(back_populates="sections")  # The department managing the section
    rides: List["Rides"] = Relationship(back_populates="section")  # Rides in this section
    shops: List["Shops"] = Relationship(back_populates="park_section")  # Shops in this section
    restaurants: List["Restaurants"] = Relationship(back_populates="park_section")  # Restaurants in this section
    entertainment: List["Entertainment"] = Relationship(back_populates="section")  # Entertainment activities in this section

    # Table-level index for the section ID
    __table_args__ = (
        Index("idx_section_id", "section_id"),  # Index on section_id for faster lookups
    )