import enum
from datetime import date 
from typing import Optional
from pydantic import BaseModel, Field

# Enum to represent the possible order statuses
class OrderStatus(str, enum.Enum):
    PENDING = "Pending"  # Order is placed but not yet processed
    SHIPPED = "Shipped"  # Order has been shipped to the customer
    RECEIVED = "Received"  # Order has been received by the customer
    CANCELLED = "Cancelled"  # Order has been cancelled


class PurchaseOrder(BaseModel):
    order_id: str 
    vendor_id: str
    order_date: date
    order_status: OrderStatus

class PurchaseOrderCreateModel(BaseModel):
    order_id: str = Field(max_length=12)
    vendor_id: str
    order_date: date

class PurchaseOrderUpdateModel(BaseModel):
    order_id: str = Field(max_length=12)
    vendor_id: str
    order_date: Optional[date] = date.today
    order_status: Optional[OrderStatus] = "Shipped"
