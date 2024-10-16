from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Vendors, PurchaseOrders

class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"
    
    invoice_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="InvoiceID"
    )
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="vendors.VendorID",
        alias="VendorID"
    )
    purchase_order: int = Field(sa_column=Column(mysql.INTEGER, nullable=False), foreign_key="purchaseorders.order_id" , alias="LineItemID")
    quantity: int = Field(sa_column=Column(mysql.INTEGER, nullable=False), alias="Quantity")
    price: float = Field(sa_column=Column(mysql.DECIMAL(10, 2), nullable=False), alias="Price")
    expected_date: Optional[date] = Field(sa_column=Column(mysql.DATE), alias="ExpectedDate")
    actual_date: datetime = Field(sa_column=Column(mysql.TIMESTAMP, nullable=False), alias="ActualDate")
    received: Optional[bool] = Field(sa_column=Column(mysql.TINYINT(1)), alias="Received")

    # Relationships
    vendor: "Vendors" = Relationship(back_populates="invoices")
    purchase_order: "PurchaseOrders" = Relationship(back_populates="invoices")
