from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import EmployeePayments, VendorPayments

# Define an Enum for payment methods
class PaymentMethodType(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    CHEQUE = "CHEQUE"
    VOUCHER = "VOUCHER"

class PaymentMethods(SQLModel, table=True):
    __tablename__ = "paymentmethods"
    
    payment_method_id: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="PaymentMethodID"
    )
    method_type: PaymentMethodType = Field(sa_column=Column(mysql.ENUM(PaymentMethodType), nullable=False), index=True, alias="MethodType")
    description: Optional[str] = Field(sa_column=Column(mysql.STRING(255)), alias="Description")  # Optional description field

    # Relationships
    employee_payments: List["EmployeePayments"] = Relationship(back_populates="payment_method", sa_relationship_kwargs={"lazy": "joined"})
    vendor_payments: List["VendorPayments"] = Relationship(back_populates="payment_method", sa_relationship_kwargs={"lazy": "joined"})
