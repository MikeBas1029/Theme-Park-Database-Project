from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class MembershipType(str, Enum):
    bronze = "Bronze"
    silver = "Silver"
    gold = "Gold"
    platinum = "Platinum"

class Customer(BaseModel):
    customer_id: int 
    first_name: str 
    last_name: str 
    email: EmailStr 
    phone_number: str 
    rewards_member: bool = False 
    address_line1: Optional[str] 
    address_line2: Optional[str] 
    city: Optional[str] 
    state: Optional[str] 
    zip_code: Optional[str] 
    country: str 
    date_of_birth: Optional[date] 
    membership_type: MembershipType
    registration_date: Optional[date] 
    renewal_date: Optional[date] 

class CustomerCreateModel(BaseModel):
    first_name: str 
    last_name: str 
    email: EmailStr 
    phone_number: str
    country: str 
    membership_type: MembershipType
    rewards_member: bool = False

class CustomerUpdateModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] 
    rewards_member: Optional[bool] 
    address_line1: Optional[str] 
    address_line2: Optional[str] 
    city: Optional[str] 
    state: Optional[str] 
    zip_code: Optional[str] 
    country: str
    date_of_birth: Optional[date] 
    membership_type: Optional[MembershipType] 
    registration_date: Optional[date] 
    renewal_date: Optional[date] 