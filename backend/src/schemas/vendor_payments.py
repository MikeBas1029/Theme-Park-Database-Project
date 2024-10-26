from datetime import date
from pydantic import BaseModel

class VendorPaymentInputModel(BaseModel):
    vendor_id: str 
    invoice_id: str 
    payment_date: date
    payment_amount: float
    payment_method_id: int

class VendorPaymentOutputModel(BaseModel):
    vendor_payment_id: str
    vendor_id: str 
    invoice_id: str 
    payment_date: date
    payment_amount: float
    payment_method_id: int
