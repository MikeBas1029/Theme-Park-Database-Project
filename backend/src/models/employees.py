from enum import Enum
from datetime import date
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import Enum as SAEnum
from pydantic import EmailStr

if TYPE_CHECKING:
    from src.models.departments import Departments
    from src.models.timesheet import Timesheet
    from src.models.employee_payments import EmployeePayments
    from src.models.guest_services import GuestServices
    from src.models.restaurants import Restaurants
    from src.models.work_orders import WorkOrders
    from src.models.shops import Shops
    from src.models.emp_auth import EmpAuth

class EmployeeType(str, Enum):
    hourly = "Hourly"
    salary = "Salary"

class Employees(SQLModel, table=True):
    __tablename__ = "employees"
    
    # SSN is the primary key for the employees table.
    # It uniquely identifies each employee in the system.
    employee_id: str = Field( 
        sa_column=Column(mysql.VARCHAR(7), primary_key=True, nullable=False, unique=True, comment="Unique employee id (primary key)"),
        alias="SSN"
    )

    # SSN is a candidate key that uniquely identifies each employee in the system.
    ssn: str = Field( 
        sa_column=Column(mysql.VARCHAR(9), unique=True, nullable=False, comment="Social Security Number (primary key)"),
        alias="SSN"
    )
    
    # FirstName is the first name of the employee.
    # This is a required field and stored as a string.
    first_name: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="First name of the employee"), alias="FirstName")
    
    # LastName is the last name of the employee.
    # This is a required field and stored as a string.
    last_name: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="Last name of the employee"), alias="LastName")
    
    # MiddleInitial is the middle initial of the employee, if available.
    # This is an optional field and stored as a single character string.
    middle_initial: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(1), comment="Middle initial of the employee"), alias="MiddleInitial")
    
    # PhoneNumber is the employee's phone number.
    # This is a required field, stored as a string.
    phone_number: str = Field(sa_column=Column(mysql.VARCHAR(15), nullable=False, comment="Phone number of the employee"), alias="PhoneNumber")
    
    # Email is the employee's email address.
    # This is a required field and validated as an email format. Must be unique.
    email: EmailStr = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False, unique=True, comment="Email address of the employee"), alias="Email")
    
    # AddressLine1 is the first line of the employee's address.
    # This is a required field, stored as a string.
    address_line1: str = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False, comment="First line of the employee's address"), alias="AddressLine1")
    
    # AddressLine2 is the second line of the employee's address, if available.
    # This is an optional field.
    address_line2: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(100), comment="Second line of the employee's address (optional)"), alias="AddressLine2")
    
    # City is the city in which the employee resides.
    # This is a required field, stored as a string.
    city: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="City of the employee's residence"), alias="City")
    
    # State is the state or province in which the employee resides.
    # This is a required field, stored as a string.
    state: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="State or province of the employee's residence"), alias="State")
    
    # ZipCode is the postal code for the employee's address.
    # This is a required field, stored as a string.
    zip_code: str = Field(sa_column=Column(mysql.VARCHAR(5), nullable=False, comment="Postal code of the employee's address"), alias="ZipCode")
    
    # Country is the country in which the employee resides.
    # This is a required field, stored as a string.
    country: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="Country of the employee's residence"), alias="Country")
    
    # Dob represents the employee's date of birth.
    # This is a required field, stored as a date value.
    dob: date = Field(sa_column=Column(mysql.DATE, nullable=False, comment="Date of birth of the employee"), alias="Dob")
    
    # StartDate represents the date when the employee started working.
    # This is a required field, stored as a date value.
    start_date: date = Field(sa_column=Column(mysql.DATE, nullable=False, comment="Date the employee started working"), alias="StartDate")
    
    # EmployeeType indicates whether the employee is hourly or salaried.
    # This is a required field, stored as a string, with an ENUM type.
    employee_type: EmployeeType = Field(
        sa_column=Column(
            SAEnum(EmployeeType, values_callable=lambda x: [e.value for e in x]),  
            nullable=False, 
            comment="Type of employee (Hourly or Salary)"
        ),
        alias="EmployeeType"
    )
    
    # HourlyWage is the employee's hourly wage, applicable only for hourly employees.
    # This is an optional field, stored as a decimal value.
    hourly_wage: Optional[float] = Field(sa_column=Column(mysql.DECIMAL(8, 2), comment="Hourly wage of the employee (for hourly employees only)"), alias="HourlyWage")
   
    salary: Optional[float] = Field(sa_column=Column(mysql.DECIMAL(9, 2), comment="Salary of the employee (for salary employees only)"), alias="Salary")
    
    # JobFunction represents the job function or title of the employee.
    # This is a required field, stored as a string.
    job_function: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="Job title or function of the employee"), alias="JobFunction")


    # Relationships
    # A department can have multiple managers (employees), and each employee can be assigned to multiple departments.
    departments: List["Departments"] = Relationship(back_populates="manager", cascade_delete=True)

    # A timesheet is created for each employee, capturing work hours and attendance.
    assigned_timesheets: List["Timesheet"] = Relationship(
        back_populates="employee", 
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "Timesheet.employee_id"},
    )

    created_timesheets: List["Timesheet"] = Relationship(
        back_populates="creator",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "Timesheet.created_by"},
    )

    updated_timesheets: List["Timesheet"] = Relationship(
        back_populates="updater",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "Timesheet.updated_by"},
    )

    worker: List["WorkOrders"] = Relationship(
        back_populates="assigned_worker",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "WorkOrders.assigned_worker_id"},
    )
    wo_creator: "WorkOrders" = Relationship(
        back_populates="creator",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "WorkOrders.created_by"},
    )
    wo_updater: "WorkOrders" = Relationship(
        back_populates="updater",
        cascade_delete=True,
        sa_relationship_kwargs={"foreign_keys": "WorkOrders.updated_by"},
    )

    managed_shops: Optional["Shops"] = Relationship(back_populates="manager")

    # An employee can have multiple payments recorded in the employee_payments table.
    employee_payments: List["EmployeePayments"] = Relationship(back_populates="employee", cascade_delete=True)

    guest_services: Optional["GuestServices"] = Relationship(back_populates="employee")

    managed_restaurants: Optional["Restaurants"] = Relationship(back_populates="manager")

    emp_auth: Optional["EmpAuth"] = Relationship(back_populates="employee")

    # Table index: Adds an index on the SSN field.
    # This index improves performance for queries filtering by SSN.
    __table_args__ = (
        Index("idx_employee_ssn", "ssn"),
    )