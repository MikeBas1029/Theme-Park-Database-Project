from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import date
from typing import Optional, List
from src.models import Visits, Tickets

class Customers(SQLModel, table=True):
    __tablename__ = "customers"
    
    customer_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="CustomerID"
    )
    first_name: str = Field(
        sa_column=Column(mysql.VARCHAR(25), nullable=False), 
        alias="FirstName"
    )
    last_name: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="LastName")
    email: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="Email")
    phone_number: str = Field(sa_column=Column(mysql.VARCHAR(15), nullable=False), alias="PhoneNumber")
    rewards_member: Optional[bool] = Field(sa_column=Column(mysql.TINYINT(1)), alias="RewardsMember")
    address_line1: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50)), alias="AddressLine1")
    address_line2: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50)), alias="AddressLine2")
    city: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(25)), alias="City")
    state: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(25)), alias="State")
    zip_code: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(5)), alias="ZipCode")
    country: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="Country")
    date_of_birth: Optional[date] = Field(sa_column=Column(mysql.DATE), alias="DateOfBirth")
    membership_type: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="MembershipType")
    registration_date: Optional[date] = Field(sa_column=Column(mysql.DATE), alias="RegistrationDate")
    renewal_date: Optional[date] = Field(sa_column=Column(mysql.DATE), alias="RenewalDate")

    # Relationships
    visits: List["Visits"] = Relationship(back_populates="customer")
    tickets: List["Tickets"] = Relationship(back_populates="customer")
