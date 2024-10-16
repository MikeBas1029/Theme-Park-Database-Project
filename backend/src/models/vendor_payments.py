from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import date
from typing import Optional
from src.models import Invoice, PaymentMethods, Vendors

class VendorPayments(SQLModel, table=True):
    __tablename__ = "vendors_payment"
    
    vendor_payment_id: int = Field(
        primary_key=True,
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="VendorPaymentID"
    )
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="vendors.VendorID",  # Link to the Vendors table
        alias="VendorID"
    )

    invoice_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="invoice.InvoiceID",
        alias="InvoiceID"
    )
    payment_date: date = Field(sa_column=Column(mysql.DATE, nullable=True), alias="PaymentDate")
    payment_amount: float = Field(sa_column=Column(mysql.DECIMAL(7, 2), nullable=True), alias="PaymentAmount")
    payment_method_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=True),
        foreign_key="paymentmethods.PaymentMethodID",
        alias="PaymentMethodID"
    )

    # Relationships
    invoice: "Invoice" = Relationship(back_populates="vendor_payments", cascade_delete=True)
    payment_method: "PaymentMethods" = Relationship(back_populates="vendor_payments")
    vendor: "Vendors" = Relationship(back_populates="vendor_payments", cascade_delete=True)