from typing import Optional
from pydantic import BaseModel 

class MerchandiseInputModel(BaseModel):
    merchandise_id: int
    item_id: str 
    subcategory: str
    size: Optional[str | None] = None
    description: str 

class MerchandiseOutputModel(BaseModel):
    merchandise_id: int
    item_id: str 
    subcategory: str
    size: str
    description: str 