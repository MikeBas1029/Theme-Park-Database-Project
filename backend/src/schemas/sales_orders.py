from datetime import date
from pydantic import BaseModel

class SalesOrdersInputModel(BaseModel):
    customer_id: str 
    order_date: date
    detail_id: str

class SalesOrdersOutputModel(BaseModel):
    transaction_id: str 
    customer_id: str 
    order_date: date
    detail_id: str