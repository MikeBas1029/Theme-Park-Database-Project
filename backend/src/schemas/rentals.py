from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel

class RentalsInputModel(BaseModel):
    rental_id: int
    item_id: str
    customer_id: str
    rental_type: str 
    start_time: datetime
    end_time: datetime 
    rental_cost: Decimal

class RentalsOutputModel(BaseModel):
    rental_id: int
    item_id: str
    customer_id: str
    rental_type: str 
    start_time: datetime # CHANGE THIS TO DATE and ADD TIME column (reflect changes in model)
    end_time: datetime  # CHANGE THIS TO DATE and ADD TIME column (reflect changes in model)
    rental_cost: Decimal