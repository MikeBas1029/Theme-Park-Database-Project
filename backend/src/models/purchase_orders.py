from enum import Enum
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

# Importing models that will be used for relationships, but only during type-checking
if TYPE_CHECKING:
    from src.models.vendors import Vendors
    from src.models.po_details import PurchaseOrderDetails

# Enum to represent the possible order statuses
class OrderStatus(str, Enum):
    PENDING = "Pending"  # Order is placed but not yet processed
    SHIPPED = "Shipped"  # Order has been shipped to the customer
    RECEIVED = "Received"  # Order has been received by the customer
    CANCELLED = "Cancelled"  # Order has been cancelled

# Main PurchaseOrders model, representing the purchase orders table in the database
class PurchaseOrders(SQLModel, table=True):
    __tablename__ = "purchaseorders"  # Name of the table in the database
    
    # order_id is the primary key for the purchase orders table, uniquely identifying each order
    order_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique ID for each purchase order"),
        alias="OrderID"  # Alias used for the column in queries
    )

    # vendor_id is a foreign key referencing the Vendors table, linking each purchase order to a specific vendor
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("vendors.vendor_id"), nullable=False, comment="ID of the vendor that created the order"),
        alias="VendorID"  # Alias used for the column in queries
    )

    # order_date is the date when the purchase order was placed. Default is set to the current UTC time
    order_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),  # Default to the current UTC time
        sa_column=Column(mysql.DATETIME, nullable=False, comment="Date when the order was placed"),
        alias="OrderDate"  # Alias used for the column in queries
    )

    # order_status is an enum field that represents the current status of the order (e.g., Pending, Shipped)
    order_status: OrderStatus = Field(
        sa_column=Column(mysql.ENUM(OrderStatus), nullable=False, comment="Status of the purchase order"),
        alias="order_status"  # Alias used for the column in queries
    )

    # Relationships
    # One purchase order is associated with one vendor (many-to-one relationship)
    vendor: "Vendors" = Relationship(back_populates="purchase_orders")  # Relationship to the Vendors model
    
    # One purchase order can have many order details (items ordered)
    order_details: List["PurchaseOrderDetails"] = Relationship(back_populates="purchase_order", cascade_delete=True)  # Relationship to the PurchaseOrderDetails model

    @property
    def total_cost(self):
        '''
        Calculates the total cost of the order based on the 
        quantity and unit price of each item in the order details.
        '''
        return sum(detail.quantity * detail.unit_price for detail in self.order_details)

    # Table arguments: Adding indexes on 'order_id' and 'vendor_id' to improve query performance
    __table_args__ = (
        Index("idx_order_id", "order_id"),
        Index("idx_vendor_id", "vendor_id")
    )