from pydantic import BaseModel

class SalesOrderDetailInputModel(BaseModel):
    item_id: str
    quantity: int 
    unit_price: float

class SalesOrderDetailOutputModel(BaseModel):
    detail_id: str
    item_id: str
    quantity: int 
    unit_price: float