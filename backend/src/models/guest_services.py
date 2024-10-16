from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Customers, Employees

class GuestServices(SQLModel, table=True):
    __tablename__ = "guestservices"
    
    service_request_id: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="ServiceRequestID"
    )
    customer_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="customers.CustomerID",
        alias="CustomerID"
    )
    request_type: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="RequestType")
    description: str = Field(sa_column=Column(mysql.TEXT, nullable=False), alias="Description")
    service_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="Date")
    employee_id: Optional[int] = Field(
        sa_column=Column(mysql.INTEGER),
        foreign_key="employees.SSN",
        alias="EmployeeID"
    )

    # Relationships
    customer: "Customers" = Relationship(back_populates="guest_services")
    employee: Optional["Employees"] = Relationship(back_populates="guest_services")
