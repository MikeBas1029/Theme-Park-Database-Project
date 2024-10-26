import string 
import secrets
import sqlalchemy.dialects.mysql as mysql
from typing import TYPE_CHECKING
from datetime import time, datetime, timedelta
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

if TYPE_CHECKING:
    from src.models.sections import Section
    from src.models.employees import Employees

class Shops(SQLModel, table=True):
    """
    Represents a shop in the theme park, including details about its location, management, 
    and operating hours.
    
    Attributes:
        shop_id (int): Unique identifier for the shop (Primary Key).
        shop_name (str): Name of the shop (e.g., "Candy Shop").
        address (str): The location/address of the shop.
        park_section_id (int): Foreign key linking the shop to a park section.
        manager_id (int): Foreign key linking the shop to the manager (employee).
        opening_time (time): The time when the shop opens.
        closing_time (time): The time when the shop closes.
    
    Relationships:
        section (Section): The section of the park where the shop is located.
        manager (Employees): The employee (manager) responsible for the shop.

    Derived Property:
        operating_hours (float): The number of operating hours for the shop, calculated 
        as the difference between the closing time and opening time. This property accounts 
        for overnight operations by adjusting for closing times that are earlier than opening times (e.g., a shop that closes past midnight).
    """
    
    __tablename__ = "shops"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    

    # Primary key for the shop
    shop_id: str = Field(
        default_factory=lambda: Shops.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12), 
            primary_key=True, 
            nullable=False,
            comment="Unique identifier for each shop in the park"
        ),
        alias="ShopID"
    )
    
    # Shop name and address
    shop_name: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, comment="Name of the shop (e.g., 'Candy Shop')"), 
        alias="ShopName"
    )
    
    address: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, comment="Location/address of the shop"), 
        alias="Location"
    )
    
    # Foreign keys linking the shop to a section and a manager
    park_section_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("sections.section_id"),  # Links to the Sections table
            nullable=False,
            comment="Foreign key linking the shop to the park section"
        ),
        alias="ParkSectionID"
    )
    
    manager_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(9), 
            ForeignKey("employees.employee_id"),  # Links to the Employees table (Manager)
            nullable=False,
            comment="Foreign key linking the shop to the employee manager"
        ),  
        alias="ManagerID"
    )
    
    # Shop opening and closing times
    opening_time: time = Field(
        sa_column=Column(mysql.TIME, nullable=False, comment="Time when the shop opens"), 
        alias="OpeningTime"
    )
    
    closing_time: time = Field(
        sa_column=Column(mysql.TIME, nullable=False, comment="Time when the shop closes"), 
        alias="ClosingTime"
    )

    # Relationships with other models
    section: "Section" = Relationship(back_populates="shops")
    manager: "Employees" = Relationship(back_populates="managed_shops")

    # Derived property to calculate operating hours as the difference between opening and closing time
    @property
    def operating_hours(self) -> float:
        """
        Calculate the operating hours of the shop as the difference between closing time and opening time.
        
        If the shop closes after midnight (i.e., the closing time is earlier than the opening time), 
        it will correctly account for the overnight operation.
        
        The calculation works by converting the `opening_time` and `closing_time` to `datetime` objects, 
        then subtracting the opening time from the closing time. If the closing time is earlier in the day 
        than the opening time (indicating an overnight shop), one day is added to the closing time.
        
        Returns:
            float: The number of operating hours, accounting for overnight operation.
        """
        # Convert time objects to datetime objects to perform arithmetic
        today = datetime.today().date()  # Get the current date
        opening_datetime = datetime.combine(today, self.opening_time)
        closing_datetime = datetime.combine(today, self.closing_time)

        # If closing time is earlier in the day than opening time, assume overnight operation
        if closing_datetime < opening_datetime:
            closing_datetime += timedelta(days=1)  # Add one day to the closing time

        # Calculate the duration between opening and closing
        operating_duration = closing_datetime - opening_datetime
        return operating_duration.total_seconds() / 3600  # Return the duration in hours
    
    # Table-level constraints and indexes for faster querying
    __table_args__ = (
        Index("idx_shop_id", "shop_id"),
        Index("idx_park_section_id", "park_section_id"),
        Index("idx_manager_id", "manager_id")
    )