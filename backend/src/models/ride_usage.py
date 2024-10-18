from datetime import time, date
from typing import TYPE_CHECKING
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

# Importing related models for type-checking
if TYPE_CHECKING:
    from src.models.rides import Rides
    from src.models.customers import Customers

class RideUsage(SQLModel, table=True):
    """
    Represents the usage of a ride by a customer. This model stores information about a specific instance
    of a customer using a ride, including the ride, customer, time spent in the queue, and date of usage.
    """
    __tablename__ = "ride_usage"  # Defines the name of the table in the database
    
    # ride_usage_id is the primary key for the ride_usage table, uniquely identifying each record of ride usage.
    ride_usage_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique ride usage ID"),
        alias="RideUsageID"
    )
    
    # customer_id references the CustomerID in the customers table, establishing a foreign key relationship.
    customer_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("customers.customer_id"), nullable=False, comment="Customer ID linked to the customer who used the ride"),
        alias="CustomerID"
    )
    
    # ride_id references the RideID in the rides table, establishing a foreign key relationship.
    ride_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("rides.ride_id"), nullable=False, comment="Ride ID linked to the specific ride used"),
        alias="RideID"
    )
    
    # usage_date stores the date when the ride usage occurred, which is mandatory.
    usage_date: date = Field(
        sa_column=Column(mysql.DATE, nullable=False, comment="Date the ride was used"),
        alias="Date"
    )
    
    # queue_time stores the time spent in the ride queue, which is mandatory.
    queue_time: time = Field(
        sa_column=Column(mysql.TIME, nullable=False, comment="Time spent waiting in the queue"),
        alias="QueueTime"
    )

    # Relationships
    # A one-to-many relationship with the Customers model, where one customer can have multiple ride usages.
    customer: "Customers" = Relationship(back_populates="ride_usages")
    
    # A one-to-many relationship with the Rides model, where one ride can have multiple ride usages.
    ride: "Rides" = Relationship(back_populates="ride_usages")

    # Indexing the `ride_id` and `usage_date` fields for faster queries filtering by these attributes.
    __table_args__ = (
        Index("idx_ride_id", "ride_id"),  
        Index("idx_usage_date", "usage_date"), 
    )