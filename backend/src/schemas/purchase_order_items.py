from pydantic import BaseModel, Field

class PurchaseOrderItemOutputModel(BaseModel):
    id: str
    item_id: str
    poid: str
    quantity: int 
    

class PurchaseOrderItemInputModel(BaseModel):
    item_id: str = Field(max_length=12)
    poid: str = Field(max_length=12)
    quantity: int 


