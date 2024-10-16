from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from typing import Optional
from datetime import time, datetime, timedelta
from src.models import Section, Employees 

class Shops(SQLModel, table=True):
    __tablename__ = "shops"
    
    # Primary key
    shop_id: int = Field(
        primary_key=True,
        sa_column=Column(mysql.INTEGER, autoincrement=True, nullable=False, index=True),
        alias="ShopID"
    )
    
    # Shop details
    shop_name: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="ShopName")
    location: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="Location")
    
    # Foreign keys
    park_section_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="sections.SectionID",
        alias="ParkSectionID"
    )
    manager_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=True),  
        foreign_key="employees.SSN",
        alias="ManagerID"
    )
    
    # Shop timings
    opening_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="OpeningTime")
    closing_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="ClosingTime")

    # Relationships
    section: "Section" = Relationship(back_populates="shops", cascade_delete=True)
    manager: Optional["Employees"] = Relationship(back_populates="managed_shops", cascade_delete=True)

    # Derived property for operating hours (calculated as the difference between closing and opening time)
    @property
    def operating_hours(self) -> float:
        """Calculate operating hours as the difference between closing time and opening time."""
        # Convert time to datetime objects
        today = datetime.today().date()  # Assuming the shop operates on the same date for calculation
        opening_datetime = datetime.combine(today, self.opening_time)
        closing_datetime = datetime.combine(today, self.closing_time)

        # If closing time is earlier in the day than opening time, assume the shop operates overnight
        if closing_datetime < opening_datetime:
            closing_datetime += timedelta(days=1)  # Adding one day to closing time if it's the next day
        
        # Calculate the difference in hours
        operating_duration = closing_datetime - opening_datetime
        return operating_duration.total_seconds() / 3600  # Convert seconds to hours