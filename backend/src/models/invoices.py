from datetime import date, datetime
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.vendors import Vendors
    from src.models.purchase_orders import PurchaseOrders
    from src.models.work_orders import WorkOrders
    from src.models.vendor_payments import VendorPayments

class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"
    
    # Invoice ID is the primary key for the invoice table. 
    # It is an auto-incrementing integer that uniquely identifies each invoice.
    invoice_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True, comment="Unique identifier for each invoice (primary key)"),
        alias="InvoiceID"
    )
    
    # Vendor ID is a foreign key referencing the Vendors table.
    # It indicates which vendor is associated with this invoice.
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("vendors.vendor_id"), nullable=False, comment="Foreign key linking to the VendorID from the vendors table"),
        alias="VendorID"
    )

    # PO (Purchase Order) number is a foreign key linking to the PurchaseOrders table.
    # It shows which purchase order this invoice is associated with.
    po_number: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("purchaseorders.order_id"), nullable=False, comment="Foreign key linking to the PurchaseOrders table (purchase order number)"), 
        alias="LineItemID"
    )

    # Quantity of items being invoiced. This field cannot be NULL.
    # It represents the number of items for this particular invoice line item.
    quantity: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False, comment="Quantity of items invoiced"),
        alias="Quantity"
    )
    
    # Price of the item being invoiced. This field cannot be NULL.
    # It stores the cost of a single unit of the item, represented as a decimal value.
    price: float = Field(
        sa_column=Column(mysql.DECIMAL(10, 2), nullable=False, comment="Price per unit of the item invoiced"),
        alias="Price"
    )

    # Expected date when the invoice items should be received.
    # This is an optional field that can be NULL if no expected date is provided.
    expected_date: Optional[date] = Field(
        sa_column=Column(mysql.DATE, comment="Expected date for the item to be received"), 
        alias="ExpectedDate"
    )
    
    # Actual date when the invoice items were received.
    # This field is mandatory and will be populated when the invoice is processed.
    actual_date: datetime = Field(
        sa_column=Column(mysql.TIMESTAMP, nullable=False, comment="Actual date when the invoice was received"),
        alias="ActualDate"
    )
    
    # A flag to indicate if the invoice has been fully received.
    # This field is optional and will be either True, False, or NULL (if not set).
    received: Optional[bool] = Field(
        sa_column=Column(mysql.TINYINT(1), comment="Indicates whether the invoice has been received (True/False)"),
        alias="Received"
    )

    # Relationships

    # Establishes a relationship between the Invoice model and the Vendors model.
    # The "vendor" field is populated with data from the "Vendors" table based on the vendor_id.
    vendor: "Vendors" = Relationship(back_populates="invoices")
    
    # Establishes a relationship between the Invoice model and the PurchaseOrders model.
    # The "purchase_order" field is populated with data from the "PurchaseOrders" table based on the po_number.
    purchase_order: "PurchaseOrders" = Relationship(back_populates="invoice")

    work_order: Optional["WorkOrders"] = Relationship(back_populates="invoices")

    vendor_payments: List["VendorPayments"] = Relationship(back_populates="invoice")

    # Table indexes: Adds indexes for the invoice_id, vendor_id, and purchase_order fields.
    # These indexes improve performance for queries filtering by these columns.
    __table_args__ = (
        Index("idx_invoice_id", "invoice_id"),
        Index("idx_vendor_id", "vendor_id"),
        Index("idx_purchase_order", "po_number")
    )