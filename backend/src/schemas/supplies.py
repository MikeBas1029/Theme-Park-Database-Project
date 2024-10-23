from typing import Optional
from pydantic import BaseModel, Field 

class Supplies(BaseModel):
    supply_id: str 
    vendor_id: str 
    name: str 
    type: str # The type or category of the supply (e.g., 'Hardware')" 
    on_hand_amount: int
    price: float

class SuppliesCreateModel(BaseModel):
    vendor_id: str = Field(max_length=12)
    name: str 
    type: str # The type or category of the supply (e.g., 'Hardware')" 
    price: float

class SuppliesUpdateModel(BaseModel):
    vendor_id: str = Field(max_length=12)
    name: str 
    type: str # The type or category of the supply (e.g., 'Hardware')" 
    on_hand_amount: int
    price: float