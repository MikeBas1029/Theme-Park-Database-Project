from datetime import time, date
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from enum import Enum
from src.models import Rides, Customers

class RideUsage(SQLModel, table=True):
    __tablename__ = "ride_usage"
    
    ride_usage_id: int = Field(
        primary_key=True,
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="RideUsageID"
    )
    customer_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="customers.CustomerID",
        alias="CustomerID"
    )
    ride_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="rides.RideID",
        alias="RideID"
    )
    usage_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="Date")
    queue_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="QueueTime")

    # Relationships
    customer: "Customers" = Relationship(back_populates="ride_usages")
    ride: "Rides" = Relationship(back_populates="ride_usages")
