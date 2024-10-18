from datetime import date
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.visits import Visits
    from src.models.tickets import Tickets

class Customers(SQLModel, table=True):
    __tablename__ = "customers"
    
    # customer_id is the primary key for the Customers table, uniquely identifying each customer.
    customer_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True, comment="Unique ID for each customer"),
        alias="CustomerID"
    )
    
    # first_name is the customer's first name, which is a required field.
    first_name: str = Field(
        sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="Customer's first name"), 
        alias="FirstName"
    )

    # last_name is the customer's last name, which is a required field.
    last_name: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="Customer's last name"), alias="LastName")
    
    # email is the customer's email address, which must be provided.
    email: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="Customer's email address"), alias="Email")
    
    # phone_number is the customer's phone number, which is a required field.
    phone_number: str = Field(sa_column=Column(mysql.VARCHAR(15), nullable=False, comment="Customer's phone number"), alias="PhoneNumber")
    
    # rewards_member indicates if the customer is a member of a rewards program (1 for true, 0 for false).
    rewards_member: Optional[bool] = Field(sa_column=Column(mysql.TINYINT(1), comment="Flag indicating whether the customer is a rewards member"), alias="RewardsMember")
    
    # address_line1 is the first line of the customer's address.
    address_line1: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), comment="First line of customer's address"), alias="AddressLine1")
    
    # address_line2 is the second line of the customer's address (optional).
    address_line2: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), comment="Second line of customer's address"), alias="AddressLine2")
    
    # city is the customer's city, an optional field.
    city: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(25), comment="Customer's city"), alias="City")
    
    # state is the customer's state, an optional field.
    state: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(25), comment="Customer's state"), alias="State")
    
    # zip_code is the customer's postal code, an optional field.
    zip_code: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(5), comment="Customer's zip code"), alias="ZipCode")
    
    # country is the customer's country, a required field.
    country: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="Customer's country"), alias="Country")
    
    # date_of_birth is the customer's date of birth (optional).
    date_of_birth: Optional[date] = Field(sa_column=Column(mysql.DATE, comment="Customer's date of birth"), alias="DateOfBirth")
    
    # membership_type defines the type of membership the customer has, such as "Standard" or "Premium".
    membership_type: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="Customer's membership type"), alias="MembershipType")
    
    # registration_date is the date when the customer registered for the service.
    registration_date: Optional[date] = Field(sa_column=Column(mysql.DATE, comment="Customer's registration date"), alias="RegistrationDate")
    
    # renewal_date is the date when the customer's membership or subscription is up for renewal.
    renewal_date: Optional[date] = Field(sa_column=Column(mysql.DATE, comment="Customer's membership renewal date"), alias="RenewalDate")


    # Relationships
    # A customer can have multiple visits, represented by the `Visits` model.
    visits: List["Visits"] = Relationship(back_populates="customer")
    
    # A customer can have multiple tickets, represented by the `Tickets` model.
    tickets: List["Tickets"] = Relationship(back_populates="customer")

    # Table index: Adds an index on the customer_id field to improve query performance.
    __table_args__ = (
        Index("idx_customer_id", "customer_id"),
    )