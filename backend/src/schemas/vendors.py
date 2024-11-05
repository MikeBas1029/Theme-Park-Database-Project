from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class VendorType(str, Enum):
    service = "Service"
    supply = "Supply"
    equipment = "Equipment"

class Vendor(BaseModel):
    vendor_id: str
    company_name: str
    vendor_contact: str 
    email: EmailStr
    phone_number: str
    address_line1: str
    address_line2: str | None 
    city: str
    state: str
    zip_code: str
    country: str
    contract_start_date: date
    contract_end_date: date
    vendor_type: VendorType

class VendorCreateModel(BaseModel):
    company_name: str
    vendor_contact: str 
    email: EmailStr
    phone_number: str
    address_line1: str
    address_line2: Optional[str | None] = None
    city: str
    state: str
    zip_code: str
    country: str
    contract_start_date: date
    contract_end_date: date
    vendor_type: VendorType

class VendorUpdateModel(BaseModel):
    company_name: str
    vendor_contact: str
    email: EmailStr
    phone_number: str
    address_line1: str
    address_line2: Optional[str | None] = None
    city: str
    state: str
    zip_code: str
    contract_start_date: date 
    contract_end_date: date 
    vendor_type: VendorType
    country: str
