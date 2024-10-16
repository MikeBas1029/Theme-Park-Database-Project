from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import date
from typing import Optional, List
from enum import Enum
from pydantic import EmailStr, validator
from src.models import Items, Supplies, PurchaseOrders, Invoice, VendorPayments
import phonenumbers

# Enum for vendor types
class VendorType(str, Enum):
    service = "Service"
    supply = "Supply"
    equipment = "Equipment"

class Vendors(SQLModel, table=True):
    __tablename__ = "vendors"
    
    vendor_id: int = Field(
        default=None,
        primary_key=True,
        index=True,
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="VendorID"
    )
    company_name: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="CompanyName")
    contact_contact: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="ContactContact")
    phone_number: str = Field(
        sa_column=Column(mysql.VARCHAR(20), nullable=False),
        alias="PhoneNumber"
    )
    email: EmailStr = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False), alias="Email")
    address_line1: str = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False), alias="AddressLine1")
    address_line2: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(100)), alias="AddressLine2")
    city: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="City")
    zip_code: str = Field(sa_column=Column(mysql.VARCHAR(10), nullable=False), alias="ZipCode")
    country: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False), alias="Country")
    vendor_type: VendorType = Field(
        sa_column=Column(mysql.ENUM(VendorType), nullable=False),
        index=True,
        alias="VendorType"
    )
    contract_start_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), index=True, alias="ContractStartDate")
    contract_end_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="ContractEndDate")
    state: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="State")

    # Relationships
    items: List["Items"] = Relationship(back_populates="vendor")
    supplies: List["Supplies"] = Relationship(back_populates="vendor")
    purchase_orders: List["PurchaseOrders"] = Relationship(back_populates="vendor")
    invoices: List["Invoice"] = Relationship(back_populates="vendor")
    vendor_payments: List["VendorPayments"] = Relationship(back_populates="vendor")  
    
    @validator("phone_number")
    def validate_phone_number(cls, v):
        try:
            # Parse the phone number
            phone = phonenumbers.parse(v, "US")  # Change the country code if needed
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone number format")
        return v