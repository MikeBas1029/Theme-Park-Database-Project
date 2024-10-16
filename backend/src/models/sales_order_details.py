from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from typing import Optional
from src.models import SalesOrders, Items 

class SalesOrderDetail(SQLModel, table=True):
    __tablename__ = "sales_order_details"
    
    # Primary key
    detail_id: int = Field(
        primary_key=True,
        sa_column=Column(
            mysql.INTEGER,
            autoincrement=True,
            nullable=False,
            comment="Unique identifier for each sales order detail",
            index=True  # Index directly in the column
        ),
        alias="DetailID"
    )

    transaction_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            nullable=False,
            comment="Foreign key referencing the sales order",
            index=True,  # Index directly in the column
            foreign_key="sales_orders.TransactionID",  # Foreign key specified here
            ondelete="CASCADE"  # Cascade delete
        ),
        alias="TransactionID"
    )

    item_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            nullable=False,
            comment="Foreign key referencing the item (SKU) in the inventory",
            index=True,  # Index directly in the column
            foreign_key="items.ItemID",  # Foreign key specified here
            ondelete="RESTRICT"  # Prevent deletion of item if referenced
        ),
        alias="ItemID"
    )

    quantity: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            nullable=False,
            comment="Number of units sold for this item",
            check="quantity > 0"  # Ensure quantity is positive
        ),
        alias="Quantity"
    )

    unit_price: float = Field(
        sa_column=Column(
            mysql.DECIMAL(10, 2),
            nullable=False,
            comment="Price per unit of the item sold",
            check="unit_price >= 0"  # Ensure unit price is non-negative
        ),
        alias="UnitPrice"
    )

    # Relationships
    sales_order: "SalesOrders" = Relationship(
        back_populates="sales_order_details", 
        cascade_delete=True,  # Cascade delete in ORM when SalesOrder is deleted
        comment="Link to the parent sales order"
    )

    item: "Items" = Relationship(
        back_populates="sales_order_details",
        comment="Link to the item in inventory"
    )

    # Derived property for subtotal
    @property
    def subtotal(self) -> float:
        """Calculate subtotal as quantity * unit price."""
        return round(self.quantity * self.unit_price, 2)  # Rounded to two decimal places for precision