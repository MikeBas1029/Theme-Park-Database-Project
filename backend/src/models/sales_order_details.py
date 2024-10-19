from typing import TYPE_CHECKING
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey, CheckConstraint

if TYPE_CHECKING:
    from src.models.sales_orders import SalesOrders
    from src.models.items import Items

class SalesOrderDetail(SQLModel, table=True):
    """
    Represents a detailed entry in a sales order, associating items with specific sales transactions.
    
    Attributes:
        detail_id (int): Unique identifier for each sales order detail (Primary Key).
        transaction_id (int): Foreign key referencing the associated sales order (SalesOrders).
        item_id (int): Foreign key referencing the item (SKU) being sold (Items).
        quantity (int): The number of units of the item sold.
        unit_price (float): The price per unit of the item.
    
    Relationships:
        sales_order (SalesOrders): Reference to the parent sales order this detail belongs to.
        item (Items): Reference to the item being sold in this detail.
    
    Table Constraints:
        - quantity > 0: Ensures the quantity is a positive integer.
        - unit_price > 0: Ensures the unit price is positive.
    
    Derived Property:
        subtotal (float): The subtotal for this sales order detail, calculated as `quantity * unit_price`.
    """
    
    __tablename__ = "sales_order_details"
    
    # Primary key
    detail_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            autoincrement=True,
            nullable=False,
            primary_key=True,
            comment="Unique identifier for each sales order detail",
        ),
        alias="DetailID"
    )

    transaction_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            ForeignKey("sales_orders.transaction_id", ondelete="CASCADE"),  # Foreign key to sales order table
            nullable=False,
            comment="Foreign key referencing the sales order",
        ),
        alias="TransactionID"
    )

    item_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            ForeignKey("items.sku", ondelete="RESTRICT"),  # Foreign key to items table (SKU reference)
            nullable=False,
            comment="Foreign key referencing the item (SKU) in the inventory",
        ),
        alias="ItemID"
    )

    quantity: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            nullable=False,
            comment="Number of units sold for this item",
        ),
        alias="Quantity"
    )

    unit_price: float = Field(
        sa_column=Column(
            mysql.DECIMAL(10, 2),
            nullable=False,
            comment="Price per unit of the item sold",
        ),
        alias="UnitPrice"
    )

    # Relationships to other tables
    sales_order: "SalesOrders" = Relationship(
        back_populates="sales_order_details",  
    )

    item: "Items" = Relationship(
        back_populates="sales_order_details",  
    )

    # Derived property for subtotal calculation
    @property
    def subtotal(self) -> float:
        """
        Calculate the subtotal for this sales order detail.
        
        Returns:
            float: The subtotal, which is the product of quantity and unit price, rounded to two decimal places.
        """
        # Calculate subtotal and round to two decimal places for precision
        return round(self.quantity * self.unit_price, 2) 
    
    __table_args__ = (
        # Indexes for faster query lookups
        Index("idx_detail_id", "detail_id"),  
        Index("idx_transaction_id", "transaction_id"),  
        Index("idx_item_id", "item_id"),  
        CheckConstraint("quantity > 0", name="chk_so_quantity_positive"),  # Constraint ensuring quantity is positive
        CheckConstraint("unit_price > 0", name="chk_so_unit_price_positive")  # Constraint ensuring unit_price is positive
    )