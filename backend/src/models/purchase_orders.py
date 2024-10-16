from typing import List
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Vendors, PurchaseOrderDetails

class OrderStatus(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    RECEIVED = "Received"
    CANCELLED = "Cancelled"

class PurchaseOrders(SQLModel, table=True):
    __tablename__ = "purchaseorders"
    
    order_id: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="OrderID"
    )
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        index=True,
        foreign_key="vendors.VendorID",
        alias="VendorID"
    )
    order_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True,
        sa_column=Column(mysql.DATETIME, nullable=False), 
        alias="OrderDate"
    )
    order_status: OrderStatus = Field(
        sa_column=Column(mysql.ENUM(OrderStatus), nullable=False), 
        alias="order_status"
    )

    # Relationships
    vendor: "Vendors" = Relationship(back_populates="purchase_orders")
    order_details: List["PurchaseOrderDetails"] = Relationship(back_populates="purchase_order", cascade_delete=True)

    @property
    def total_cost(self):
        return sum(detail.quantity * detail.unit_price for detail in self.order_details)