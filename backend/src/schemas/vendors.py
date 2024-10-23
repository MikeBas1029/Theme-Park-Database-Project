from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class VendorType(str, Enum):
    service = "Service"
    supply = "Supply"
    equipment = "Equipment"

class Vendor(BaseModel):
    vendor_id: int
    company_name: str
    email: EmailStr
    phone_number: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: str
    contract_start: Optional[date | None] = None
    contract_end: Optional[date | None] = None
    vendor_type: VendorType

class VendorCreateModel(BaseModel):
    vendor_id: int
    company_name: str
    email: EmailStr
    phone_number: str
    country: str

class VendorUpdateModel(BaseModel):
    email: EmailStr
    phone_number: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    contract_start: Optional[date] = None
    contract_end: Optional[date] = None
    vendor_type: VendorType
    country: str
