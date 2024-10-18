from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.employee_payments import EmployeePayments
    from src.models.vendor_payments import VendorPayments

# Define an Enum for payment methods
class PaymentMethodType(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    CHEQUE = "CHEQUE"
    VOUCHER = "VOUCHER"

class PaymentMethods(SQLModel, table=True):
    __tablename__ = "paymentmethods"
    
    # payment_method_id is the primary key for the PaymentMethods table, uniquely identifying each payment method.
    payment_method_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique ID for each payment method"),
        alias="PaymentMethodID"
    )
    
    # method_type is an Enum representing the type of payment method (e.g., CASH, CARD, BANK_TRANSFER).
    method_type: PaymentMethodType = Field(
        sa_column=Column(mysql.ENUM(PaymentMethodType), nullable=False, comment="Type of payment method"), 
        alias="MethodType"
    )
    
    # description provides additional information about the payment method (e.g., "Credit card payments").
    description: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(255), comment="Description of the payment method"), 
        alias="Description"
    )

    # Relationships
    # An employee payment can be made using one of the payment methods. This relationship connects to the EmployeePayments table.
    employee_payments: List["EmployeePayments"] = Relationship(
        back_populates="payment_method", 
    )
    
    # A vendor payment can be made using one of the payment methods. This relationship connects to the VendorPayments table.
    vendor_payments: List["VendorPayments"] = Relationship(
        back_populates="payment_method", 
    )
