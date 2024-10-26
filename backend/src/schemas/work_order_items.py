from typing import Optional
from pydantic import BaseModel

class WorkOrderItemInputModel(BaseModel):
    woid: str 
    po_item_id: Optional[str]

class WorkOrderItemOutputModel(BaseModel):
    id: str
    woid: str 
    po_item_id: Optional[str]