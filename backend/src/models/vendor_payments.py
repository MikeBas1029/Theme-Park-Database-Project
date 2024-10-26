import string 
import secrets
from datetime import date
import sqlalchemy.dialects.mysql as mysql
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

if TYPE_CHECKING:
    from src.models.invoices import Invoice
    from src.models.payment_methods import PaymentMethods
    from src.models.vendors import Vendors

class VendorPayments(SQLModel, table=True):
    """
    Represents a payment made to a vendor for an invoice. This model links the payment details 
    to the associated vendor, invoice, and payment method, allowing tracking of payments 
    made by the organization to its vendors.

    Attributes:
        vendor_payment_id (int): Unique identifier for the payment record (Primary Key).
        vendor_id (int): Foreign key linking to the vendor receiving the payment.
        invoice_id (int): Foreign key linking to the invoice associated with this payment.
        payment_date (date): The date when the payment was made.
        payment_amount (float): The amount paid to the vendor.
        payment_method_id (int): Foreign key linking to the payment method used.

    Relationships:
        invoice (Invoice): Reference to the associated invoice for this payment.
        payment_method (PaymentMethods): Reference to the method used for the payment.
        vendor (Vendors): Reference to the vendor receiving the payment.
    """
    
    __tablename__ = "vendor_payments"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    

    # Primary key for the vendor payment
    vendor_payment_id: str = Field(
        default_factory=lambda: VendorPayments.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12), 
            primary_key=True, 
            nullable=False,
            comment="Unique identifier for each vendor payment"
        ),
        alias="VendorPaymentID"
    )
    
    # Foreign key linking to the Vendor receiving the payment
    vendor_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12), 
            ForeignKey("vendors.vendor_id"),  
            nullable=False,
            comment="Foreign key linking to the Vendor receiving the payment"
        ),
        alias="VendorID"
    )

    # Foreign key linking to the Invoice being paid
    invoice_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12), 
            ForeignKey("invoice.invoice_id"),
            nullable=False,
            comment="Foreign key linking to the associated invoice"
        ),
        alias="InvoiceID"
    )
    
    # Date when the payment was made
    payment_date: date = Field(
        sa_column=Column(mysql.DATE, nullable=False, comment="Date when the payment was made"), 
        alias="PaymentDate"
    )
    
    # The amount of money paid to the vendor
    payment_amount: float = Field(
        sa_column=Column(mysql.DECIMAL(7, 2), nullable=False, comment="Amount paid to the vendor"), 
        alias="PaymentAmount"
    )
    
    # Foreign key linking to the PaymentMethod used for this transaction
    payment_method_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("paymentmethods.payment_method_id"),
            nullable=False,
            comment="Foreign key linking to the payment method used"
        ),
        alias="PaymentMethodID"
    )

    # Relationships

    # Relationship with the Invoice model to retrieve the associated invoice for this payment
    invoice: "Invoice" = Relationship(
        back_populates="vendor_payments", 
    )
    
    # Relationship with the PaymentMethods model to get the payment method used
    payment_method: "PaymentMethods" = Relationship(
        back_populates="vendor_payments",
        sa_relationship_kwargs={"lazy": "joined"},  # Eager loading with JOIN to optimize queries
    )
    
    # Relationship with the Vendors model to retrieve vendor details for this payment
    vendor: "Vendors" = Relationship(
        back_populates="vendor_payments",
    )

    # Table indexes to optimize queries based on commonly searched fields
    __table_args__ = (
        Index("idx_vendor_payment_id", "vendor_payment_id"),
        Index("idx_vendor_id", "vendor_id"),
        Index("idx_invoice_id", "invoice_id")
    )