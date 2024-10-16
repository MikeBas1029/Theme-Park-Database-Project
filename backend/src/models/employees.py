from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import date
from typing import Optional, List
from src.models import Departments, Timesheet, EmployeePayments
from pydantic import EmailStr

class Employees(SQLModel, table=True):
    __tablename__ = "employees"
    
    ssn: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="SSN"
    )
    first_name: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="FirstName")
    last_name: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="LastName")
    middle_initial: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(1)), alias="MiddleInitial")
    phone_number: str = Field(sa_column=Column(mysql.VARCHAR(15), nullable=False), alias="PhoneNumber")
    email: EmailStr = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False), alias="Email")
    address_line1: str = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False), alias="AddressLine1")
    address_line2: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(100)), alias="AddressLine2")
    city: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="City")
    state: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="State")
    zip_code: str = Field(sa_column=Column(mysql.VARCHAR(5), nullable=False), alias="ZipCode")
    country: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="Country")
    dob: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="Dob")
    start_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="StartDate")
    employee_type: str = Field(sa_column=Column(mysql.ENUM("Hourly", "Salary"), nullable=False), alias="EmployeeType")
    hourly_wage: Optional[float] = Field(sa_column=Column(mysql.DECIMAL(8, 2)), alias="HourlyWage")
    job_function: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="JobFunction")

    # Relationships
    departments: List["Departments"] = Relationship(back_populates="manager", cascade_delete=True)
    timesheets: List["Timesheet"] = Relationship(back_populates="employee", cascade_delete=True)
    employee_payments: List["EmployeePayments"] = Relationship(back_populates="employee", cascade_delete=True)