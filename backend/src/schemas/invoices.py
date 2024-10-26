from pydantic import BaseModel 
from datetime import date 
from typing import Optional
from enum import Enum 

class PaymentStatus(str, Enum):
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

class Invoice(BaseModel):
    invoice_id: str 
    po_number: str 
    amount_due: float 
    issue_date: date
    due_date: Optional[date]
    payment_status: PaymentStatus 

class InvoiceCreateModel(BaseModel):
    po_number: str 
    amount_due: float 
    issue_date: date
    due_date: Optional[date | None] = None
    payment_status: PaymentStatus 

class InvoiceUpdateModel(BaseModel):
    po_number: str 
    amount_due: Optional[float]
    issue_date: Optional[date | None] = None
    due_date: Optional[date | None] = None
    payment_status: PaymentStatus 