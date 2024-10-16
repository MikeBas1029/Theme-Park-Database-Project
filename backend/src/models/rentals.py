from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from pydantic import root_validator
from decimal import Decimal
from src.models import Items, Customers

class Rentals(SQLModel, table=True):
    __tablename__ = "rentals"
    
    item_id: int = Field(
        primary_key=True,
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="items.SKU",  
        alias="ItemID",
        index=True  
    )
    customer_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="customers.CustomerID",
        alias="CustomerID",
        index=True 
    )
    rental_type: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="RentalType")
    start_time: datetime = Field(
        sa_column=Column(mysql.DATETIME, nullable=False), 
        alias="StartTime"
    )
    end_time: datetime = Field(
        sa_column=Column(mysql.DATETIME, nullable=False), 
        alias="EndTime"
    )

    rental_cost: Optional[Decimal] = Field(sa_column=Column(mysql.DECIMAL(10, 2)), alias="RentalCost")
    
    # Relationships
    item: "Items" = Relationship(back_populates="rentals")
    customer: "Customers" = Relationship(back_populates="rentals")
    
    # Validation to ensure start_time is before end_time
    @root_validator
    def check_rental_times(cls, values):
        start_time = values.get('start_time')
        end_time = values.get('end_time')
        if start_time and end_time and start_time >= end_time:
            raise ValueError('Start time must be before end time.')
        return values
    
    @property
    def rental_duration(self) -> Optional[int]:
        """Calculates the rental duration in minutes."""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() // 60)  # returns duration in minutes
        return None