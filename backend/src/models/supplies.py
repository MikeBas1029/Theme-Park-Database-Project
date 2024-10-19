from decimal import Decimal
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey, CheckConstraint

if TYPE_CHECKING:
    from src.models.vendors import Vendors
    from src.models.po_details import PurchaseOrderDetails

class Supplies(SQLModel, table=True):
    """
    Represents a supply item within the inventory, including details such as the supply's 
    vendor, invoice, type, stock level, and price.

    Attributes:
        supply_id (int): Unique identifier for the supply (Primary Key).
        vendor_id (int): Foreign key linking the supply to the vendor providing it.
        invoice_id (Optional[int]): Foreign key linking the supply to a specific invoice.
        name (str): The name of the supply (e.g., "Widget").
        type (str): The type/category of the supply (e.g., "Hardware").
        on_hand_amount (int): The quantity of the supply currently in stock.
        price (float): The unit price of the supply.

    Relationships:
        vendor (Vendors): The vendor that supplies this item.
        invoice (Invoice): The invoice associated with the supply (if available).
        order_details (List[PurchaseOrderDetails]): The details of purchase orders that include this supply.

    Derived Properties:
        total_value (Decimal): The total value of the supplies on hand, calculated 
        as the product of the unit price and the quantity on hand.
    """
    
    __tablename__ = "supplies"
    
    # Primary key for the supply
    supply_id: int = Field(
        default=None,
        sa_column=Column(
            mysql.INTEGER,  # MySQL integer type
            primary_key=True,  # Primary key constraint
            nullable=False,  # This column cannot be null
            autoincrement=True,  # Auto-increment value for new rows
            comment="Unique identifier for each supply item"  # Comment for documentation
        ),
        alias="SupplyID"
    )
    
    # Foreign keys to vendor and invoice tables
    vendor_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,  # Integer type for vendor ID
            ForeignKey("vendors.vendor_id"),  # Foreign key reference to the Vendor table
            nullable=False,  # This column cannot be null
            comment="Foreign key linking supply to the vendor providing it"  # Comment
        ),
        alias="VendorID"
    )
    
    # Supply details
    name: str = Field(
        sa_column=Column(
            mysql.VARCHAR(25),  # String column, max length of 25
            nullable=False,  # This column cannot be null
            comment="The name of the supply item (e.g., 'Widget')"  # Comment
        ), 
        alias="Name"
    )
    type: str = Field(
        sa_column=Column(
            mysql.VARCHAR(25),  # String column, max length of 25
            nullable=False,  # This column cannot be null
            comment="The type or category of the supply (e.g., 'Hardware')"  # Comment
        ), 
        alias="Type"
    )
    
    # Stock and price details
    on_hand_amount: int = Field(
        sa_column=Column(
            mysql.INTEGER,  # Integer type for quantity of stock
            nullable=False,  # This column cannot be null
            comment="Quantity of the supply currently in stock"  # Comment
        ),  
        alias="OnHandAmount"
    )
    price: float = Field(
        sa_column=Column(
            mysql.FLOAT,  # Float type for price value
            nullable=False,  # This column cannot be null
            comment="The unit price of the supply item"  # Comment
        ), 
        alias="Price"
    )
    
    # Relationships with other models
    vendor: "Vendors" = Relationship(
        back_populates="supplies", 
    )
    order_details: "PurchaseOrderDetails" = Relationship(
        back_populates="supplies", 
    )

    # Derived property for calculating the total value of supplies on hand
    @property
    def total_value(self) -> Decimal:
        """
        Calculate the total value of the supplies on hand by multiplying the unit price 
        by the quantity of supplies in stock.

        This derived property helps to quickly calculate the financial value of all available 
        supplies in the inventory. The result is rounded to two decimal places to ensure 
        precision for monetary calculations.
        
        Returns:
            Decimal: The total value of the supplies on hand, calculated as price * quantity, 
            rounded to two decimal places.
        """
        return round(Decimal(self.on_hand_amount) * Decimal(self.price), 2)

    # Optional string representation for easier debugging/logging
    def __repr__(self):
        return f"<Supply(id={self.supply_id}, name={self.name}, type={self.type}, on_hand_amount={self.on_hand_amount}, price={self.price})>"
    
    __table_args__ = (
        # Indexes for optimizing queries
        Index("idx_supply_id", "supply_id"),  # Index for the supply_id column
        Index("idx_vendor_id", "vendor_id"),  # Index for the vendor_id column
        
        # Check constraints to ensure data validity
        CheckConstraint("on_hand_amount >= 0", name="chk_oh_positive"),  # Ensure on_hand_amount is non-negative
        CheckConstraint("price >= 0", name="chk_price_positive")  # Ensure price is non-negative
    )