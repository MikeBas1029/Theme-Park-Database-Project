from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, List
from decimal import Decimal
from src.models import Vendors, Invoice, PurchaseOrderDetails

class Supplies(SQLModel, table=True):
    __tablename__ = "supplies"
    
    # Primary key
    supply_id: int = Field(
        default=None,
        primary_key=True,
        index=True,  # Index to speed up queries involving the supply ID
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="SupplyID"
    )
    
    # Supply details
    name: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="Name")
    type: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="Type")
    
    # Stock and price details
    on_hand_amount: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False, check="on_hand_amount >= 0"),  # Ensure non-negative stock
        alias="OnHandAmount"
    )
    price: float = Field(
        sa_column=Column(mysql.FLOAT, nullable=False, check="price >= 0"),  # Ensure non-negative price
        alias="Price"
    )
    
    # Foreign keys
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="vendors.VendorID",
        index=True,  # Index for foreign key to speed up queries
        alias="VendorID"
    )

    invoice_id: Optional[int] = Field(
        sa_column=Column(mysql.INTEGER, nullable=True),
        foreign_key="invoice.InvoiceID",
        index=True,  # Index for optional foreign key
        alias="InvoiceID"
    )
    
    # Relationships
    vendor: "Vendors" = Relationship(back_populates="supplies", cascade_delete=True)
    invoice: Optional["Invoice"] = Relationship(back_populates="supplies")
    order_details: List["PurchaseOrderDetails"] = Relationship(back_populates="supply", cascade_delete=True)

    # Derived property for total value of supplies on hand
    @property
    def total_value(self) -> Decimal:
        """Calculate the total value of the supplies on hand (price * quantity)."""
        return round(Decimal(self.on_hand_amount) * Decimal(self.price), 2)

    # Optional: Adding a string representation for debugging and logging
    def __repr__(self):
        return f"<Supply(id={self.supply_id}, name={self.name}, type={self.type}, on_hand_amount={self.on_hand_amount}, price={self.price})>"