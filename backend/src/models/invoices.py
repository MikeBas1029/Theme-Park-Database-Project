import enum
from datetime import date, datetime
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import Enum as SAEnum

if TYPE_CHECKING:
    from src.models.vendors import Vendors
    from src.models.purchase_orders import PurchaseOrders
    from src.models.work_orders import WorkOrders
    from src.models.vendor_payments import VendorPayments

class PaymentStatus(str, enum.Enum):
    paid = "paid" # full payment received and processed
    partial = "partial" # partial payment but balance still outstanding
    pending = "pending" # invoice generate but not paid yet
    overdue = "overdue" # payment due but not paid yet
    canceled = "canceled" # invoice canceled after created no payment due
    failed = "failed" # payment attempted but failed
    refunded = "refunded" # payment made but later refunded
    disputed = "disputed" # customer has raised an issue 
    awaiting = "awaiting" # invoice sent to customer, payment still expected
    void = "void" # never processed


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

    # Amount being invoiced. This field cannot be NULL.
    # It stores the total amount of the item or service, represented as a decimal value.
    amount_due: float = Field(
        sa_column=Column(mysql.DECIMAL(10, 2), nullable=False, comment="Price per unit of the item invoiced"),
        alias="Price"
    )

    issue_date: date = Field(
        sa_column=Column(mysql.DATE, comment="Date invoice was generated."), 
        alias="IssueDate"
    )

    due_date: Optional[date] = Field(
        sa_column=Column(
            mysql.DATE, 
            nullable=True,
            comment="Expected date for the invoice to be paid."
        ), 
        alias="DueDate"
    )

    payment_status: PaymentStatus = Field(
        sa_column=Column(
            SAEnum(PaymentStatus, values_callable=lambda x: [e.value for e in x]),
            nullable=False,
            comment="The current status of the invoice."
        )
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