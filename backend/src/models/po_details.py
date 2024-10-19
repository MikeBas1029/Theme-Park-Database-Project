from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey, CheckConstraint
import sqlalchemy.dialects.mysql as mysql

# Importing models that will be used for relationships, but only during type-checking
if TYPE_CHECKING:
    from src.models.supplies import Supplies
    from src.models.purchase_orders import PurchaseOrders

class PurchaseOrderDetails(SQLModel, table=True):
    __tablename__ = "orderdetails"  # Name of the table in the database
    
    # order_details_id is the primary key for the order details, uniquely identifying each record.
    order_details_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique ID for each order detail"),
        alias="OrderDetailsID"
    )
    
    # order_id is a foreign key referencing the PurchaseOrders table, linking each order detail to a specific order.
    order_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("purchaseorders.order_id"), nullable=False, comment="ID of the related purchase order"),
        alias="OrderID"
    )
    
    # supply_id is a foreign key referencing the Supplies table, linking each order detail to a specific supply.
    supply_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("supplies.supply_id"), nullable=False, comment="ID of the related supply"),
        alias="SupplyID"
    )
    
    # quantity is the number of units of the supply in this order detail. It cannot be negative.
    quantity: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False, comment="Quantity of the supply in the order detail"),
        alias="Quantity"
    )
    
    # unit_price is the price per unit of the supply in this order detail. It cannot be negative.
    unit_price: float = Field(
        sa_column=Column(mysql.DECIMAL(10, 2), nullable=False, comment="Price per unit of the supply in the order detail"),
        alias="UnitPrice"
    )

    # subtotal is a calculated property that returns the total price for this order detail (quantity * unit price).
    @property
    def subtotal(self): 
        return self.quantity * self.unit_price

    # Relationships
    # The PurchaseOrderDetails table is linked to the PurchaseOrders table (one-to-many relationship).
    purchase_order: "PurchaseOrders" = Relationship(back_populates="order_details")
    
    # The PurchaseOrderDetails table is linked to the Supplies table (one-to-many relationship).
    supplies: "Supplies" = Relationship(back_populates="order_details")

    # Table indexes and constraints
    __table_args__ = (
        # Adds an index to improve the performance of queries 
        Index("idx_order_details_id", "order_details_id"),
        Index("idx_order_id", "order_id"),
        Index("idx_supply_id", "supply_id"),
        
        # Ensures the quantity is always greater than zero (check constraint)
        CheckConstraint("quantity > 0", name="chk_po_quantity_positive"),
        
        # Ensures the unit price is always greater than zero (check constraint)
        CheckConstraint("unit_price > 0", name="chk_po_unit_price_positive"),
    )