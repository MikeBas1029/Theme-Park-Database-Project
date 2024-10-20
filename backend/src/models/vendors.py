import phonenumbers
import enum
from datetime import date
from pydantic import EmailStr, validator
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
from sqlalchemy import Enum as SAEnum

if TYPE_CHECKING:
    from src.models.items import Items 
    from src.models.supplies import Supplies
    from src.models.purchase_orders import PurchaseOrders
    from src.models.invoices import Invoice
    from src.models.vendor_payments import VendorPayments


# Enum for vendor types
class VendorType(str, enum.Enum):
    """
    Enum representing the types of vendors in the system.

    Attributes:
        service (str): Vendor providing services.
        supply (str): Vendor supplying goods.
        equipment (str): Vendor supplying equipment.
    """
    service = "Service"
    supply = "Supply"
    equipment = "Equipment"


class Vendors(SQLModel, table=True):
    """
    Represents a vendor in the system, including details about the vendor's company, contact information,
    contract details, and relationships with other entities.

    Attributes:
        vendor_id (int): Unique identifier for the vendor.
        company_name (str): The name of the vendor's company.
        vendor_contact (str): The contact person's name at the vendor.
        phone_number (str): The contact phone number of the vendor.
        email (EmailStr): The contact email address for the vendor.
        address_line1 (str): The first line of the vendor's address.
        address_line2 (Optional[str]): The second line of the vendor's address (optional).
        city (str): The city where the vendor is located.
        zip_code (str): The zip code of the vendor's address.
        country (str): The country where the vendor is located.
        vendor_type (VendorType): The type of vendor (Service, Supply, Equipment).
        contract_start_date (date): The start date of the vendor's contract.
        contract_end_date (date): The end date of the vendor's contract.
        state (str): The state where the vendor is located.

    Relationships:
        items (List[Items]): A list of items provided by the vendor.
        supplies (List[Supplies]): A list of supplies provided by the vendor.
        purchase_orders (List[PurchaseOrders]): A list of purchase orders associated with the vendor.
        invoices (List[Invoice]): A list of invoices from the vendor.
        vendor_payments (List[VendorPayments]): A list of payments made to the vendor.

    Methods:
        validate_phone_number: Validates the phone number format using the `phonenumbers` library.
    
    Indexes:
        idx_vendor_id: Index on the vendor ID for faster querying.
        idx_contract_start_date: Index on the contract start date for efficient contract date searches.
    """
    
    __tablename__ = "vendors"
    
    vendor_id: int = Field(
        default=None,
        sa_column=Column(
            mysql.INTEGER, 
            nullable=False, 
            primary_key=True, 
            autoincrement=True,
            comment="Unique identifier for the vendor"
        ),
        alias="VendorID"
    )
    
    company_name: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, comment="The name of the vendor's company"), 
        alias="CompanyName"
    )
    
    vendor_contact: str = Field(
        sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="The contact person's name at the vendor"), 
        alias="VendorContact"
    )
    
    phone_number: str = Field(
        sa_column=Column(mysql.VARCHAR(20), nullable=False, comment="The contact phone number of the vendor"),
        alias="PhoneNumber"
    )
    
    email: EmailStr = Field(
        sa_column=Column(mysql.VARCHAR(100), nullable=False, comment="The contact email address for the vendor"),
        alias="Email"
    )
    
    address_line1: str = Field(
        sa_column=Column(mysql.VARCHAR(100), nullable=False, comment="The first line of the vendor's address"),
        alias="AddressLine1"
    )
    
    address_line2: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(100), comment="The second line of the vendor's address (optional)"), 
        alias="AddressLine2"
    )
    
    city: str = Field(
        sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="The city where the vendor is located"), 
        alias="City"
    )
    
    zip_code: str = Field(
        sa_column=Column(mysql.VARCHAR(10), nullable=False, comment="The zip code of the vendor's address"),
        alias="ZipCode"
    )
    
    country: str = Field(
        sa_column=Column(mysql.VARCHAR(50), nullable=False, comment="The country where the vendor is located"), 
        alias="Country"
    )
    
    vendor_type: VendorType = Field(
        sa_column=Column(
            SAEnum(VendorType, values_callable=lambda x: [e.value for e in x]), 
            nullable=False, 
            comment="The type of vendor (Service, Supply, Equipment)"
        ),
        alias="VendorType"
    )
    
    contract_start_date: date = Field(
        sa_column=Column(mysql.DATE, nullable=False, comment="The start date of the vendor's contract"), 
        alias="ContractStartDate"
    )
    
    contract_end_date: date = Field(
        sa_column=Column(mysql.DATE, nullable=False, comment="The end date of the vendor's contract"), 
        alias="ContractEndDate"
    )
    
    state: str = Field(
        sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="The state where the vendor is located"), 
        alias="State"
    )

    # Relationships
    items: List["Items"] = Relationship(
        back_populates="vendor", 
    )
    
    supplies: List["Supplies"] = Relationship(
        back_populates="vendor", 
    )
    
    purchase_orders: List["PurchaseOrders"] = Relationship(
        back_populates="vendor", 
    )
    
    invoices: List["Invoice"] = Relationship(
        back_populates="vendor", 
    )
    
    vendor_payments: List["VendorPayments"] = Relationship(
        back_populates="vendor", 
        cascade_delete=True,
    )

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """
        Validates the phone number format using the `phonenumbers` library.
        
        Args:
            v (str): The phone number to validate.

        Returns:
            str: The validated phone number.

        Raises:
            ValueError: If the phone number is invalid or in an incorrect format.
        """
        try:
            # Parse the phone number
            phone = phonenumbers.parse(v, "US")  # Change the country code if needed
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone number format")
        return v
    
    __table_args__ = (
        Index("idx_vendor_id", "vendor_id"),
        Index("idx_contract_start_date", "contract_start_date"),
    )