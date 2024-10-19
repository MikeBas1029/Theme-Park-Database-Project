from datetime import date
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.customers import Customers
    from src.models.employees import Employees

class GuestServices(SQLModel, table=True):
    __tablename__ = "guestservices"
    
    # ServiceRequestID is the primary key for the guest services table.
    # It uniquely identifies each guest service request.
    service_request_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique identifier for each guest service request (primary key)"),
        alias="ServiceRequestID"
    )

    # CustomerID is a foreign key referencing the Customers table.
    # It associates each service request with a specific customer.
    customer_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("customers.customer_id"), nullable=False, comment="Foreign key linking to the CustomerID from the customers table"),
        alias="CustomerID"
    )

    # RequestType is a short description of the type of service request.
    # It cannot be NULL.
    request_type: str = Field(
        sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="Type of service request (e.g., complaint, request, inquiry)"),
        alias="RequestType"
    )

    # Description is a detailed explanation of the guest service request.
    # It cannot be NULL and is stored as text for flexibility.
    description: str = Field(
        sa_column=Column(mysql.TEXT, nullable=False, comment="Detailed description of the service request"),
        alias="Description"
    )

    # ServiceDate is the date when the service request was made or processed.
    # It cannot be NULL and must be a valid date.
    service_date: date = Field(
        sa_column=Column(mysql.DATE, nullable=False, comment="Date when the service request was made or processed"),
        alias="Date"
    )

    # EmployeeID is an optional foreign key referencing the Employees table.
    # It associates an employee with the service request. If NULL, no employee is associated.
    employee_id: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(9), ForeignKey("employees.ssn"), comment="Foreign key linking to the Employees table (employee assigned to the service request)"),
        alias="EmployeeID"
    )

    # Relationships

    # Establishes a relationship between the GuestServices model and the Customers model.
    # The "customer" field is populated with data from the "Customers" table based on the customer_id.
    customer: "Customers" = Relationship(back_populates="guest_services")
    
    # Establishes a relationship between the GuestServices model and the Employees model.
    # The "employee" field is populated with data from the "Employees" table based on the employee_id.
    employee: List["Employees"] = Relationship(back_populates="guest_services")

    # Table index: Adds an index for the service_request_id field.
    # This index improves performance for queries filtering by service_request_id.
    __table_args__ = (
        Index("idx_service_request_id", "service_request_id"),
    )