from enum import Enum
from pydantic import BaseModel
from typing import Optional

class ItemCategory(str, Enum):
    merch = "Merchandise"
    concession = "Concession"
    entertainment = "Entertainment"
    other = "Other"

class ItemStatus(str, Enum):
    active = "Active"
    discontinued = "Discontinued"
    backorder = "Backorder"

class ItemBase(BaseModel):
    name: str
    category: ItemCategory
    price: float
    cost: float
    status: ItemStatus
    vendor_id: int

class Item(ItemBase):
    sku: int
    class Config:
        orm_mode = True

# Schema for creating an item
class ItemCreateModel(ItemBase):
    pass  # All fields from ItemBase are required for creation

# Schema for updating an item
class ItemUpdateModel(BaseModel):
    name: Optional[str]
    category: Optional[ItemCategory]
    price: Optional[float]
    cost: Optional[float]
    status: Optional[ItemStatus]
    vendor_id: Optional[int]