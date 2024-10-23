from enum import Enum
from pydantic import BaseModel
from typing import Optional


class BeverageType(str, Enum):
    soda = "Soda"
    juice = "Juice"
    water = "Water"
    other = "Other"

class Beverage(BaseModel):
    bev_id: int 
    sku: str 
    drink_size: str
    beverage_item: BeverageType 
    calories: int

class BeverageCreateModel(BaseModel):
    sku: str 
    drink_size: str
    beverage_item: BeverageType 


class BeverageUpdateModel(BaseModel):
    sku: str 
    drink_size: Optional[str]
    beverage_item: Optional[BeverageType]
    calories: Optional[int]
