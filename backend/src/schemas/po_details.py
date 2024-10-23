from pydantic import BaseModel, Field

class PurchaseOrderDetailsOutputModel(BaseModel):
    order_details_id: str
    order_id: str
    supply_id: str 
    quantity: int
    unit_price: float

class PurchaseOrderDetailsInputModel(BaseModel):
    order_id: str
    supply_id: str 
    quantity: int