from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql
from pydantic import model_validator
from decimal import Decimal

# Importing related models for type-checking
if TYPE_CHECKING:
    from src.models.items import Items
    from src.models.customers import Customers

class Rentals(SQLModel, table=True):
    """
    Represents the rental records for items by customers. The model stores information 
    such as rental details, customer information, rental duration, and costs.
    """
    __tablename__ = "rentals"  # Defines the name of the table in the database

    # rental_id is the primary key for the rentals table. This uniquely identifies each rental record.
    rental_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, autoincrement=True, nullable=False, comment="Unique rental ID, auto-incremented"),
        alias="RentalID"
    )
    
    # item_id is a foreign key linking to the Items table. It represents the item being rented.
    item_id: str = Field(
        sa_column=Column(mysql.VARCHAR(12), ForeignKey("items.sku"), nullable=False, comment="ID of the rented item, linked to Items table"),
        alias="ItemID",
    )
    
    # customer_id is a foreign key linking to the Customers table. It represents the customer renting the item.
    customer_id: str = Field(
        sa_column=Column(mysql.VARCHAR(12), ForeignKey("customers.customer_id"), nullable=False, comment="ID of the customer renting the item, linked to Customers table"),
        alias="CustomerID",
    )
    
    # rental_type represents the type of rental (e.g., short-term, long-term, etc.)
    rental_type: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, comment="Type of rental (e.g., short-term, long-term)"),
        alias="RentalType"
    )
    
    # start_time represents the date and time when the rental starts.
    start_time: datetime = Field(
        sa_column=Column(mysql.DATETIME, nullable=False, comment="Start time of the rental"),
        alias="StartTime"
    )
    
    # end_time represents the date and time when the rental ends.
    end_time: datetime = Field(
        sa_column=Column(mysql.DATETIME, nullable=False, comment="End time of the rental"),
        alias="EndTime"
    )

    # rental_cost represents the total cost for the rental, calculated based on duration and rental type.
    rental_cost: Decimal = Field(
        sa_column=Column(mysql.DECIMAL(10, 2), nullable=False, comment="Total cost of the rental"),
        alias="RentalCost"
    )
    
    # Relationships
    item: "Items" = Relationship(back_populates="rentals")  # One-to-many relationship with the Items table.
    customer: "Customers" = Relationship(back_populates="rentals")  # One-to-many relationship with the Customers table.
    
    # Validator to ensure that the start_time is before the end_time for each rental.
    @model_validator(mode='before')
    @classmethod
    def check_rental_times(cls, values):
        """
        Validates that the start time of the rental is before the end time.
        
        Args:
            cls: The class reference.
            values: The values dictionary containing the fields of the model.
            
        Raises:
            ValueError: If the start time is not before the end time.
        
        Returns:
            The validated values dictionary.
        """
        start_time = values.get('start_time')
        end_time = values.get('end_time')
        
        # Check if start_time is greater than or equal to end_time and raise an error if so
        if start_time and end_time and start_time >= end_time:
            raise ValueError('Start time must be before end time.')
        
        return values
    
    @property
    def rental_duration(self) -> Optional[int]:
        """
        Calculates the rental duration in minutes.
        
        This property computes the difference between the start time and end time
        and returns it as the rental duration in minutes.
        
        Returns:
            int: The rental duration in minutes, or None if times are not set.
        """
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() // 60)  # Converts the duration from seconds to minutes
        return None
    
    __table_args__ = (
        Index("idx_rental_id", "rental_id"),
        Index("idx_item_id", "item_id"),
        Index("idx_customer_id", "customer_id")
    )