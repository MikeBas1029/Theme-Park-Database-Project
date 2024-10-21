from enum import Enum 
from pydantic import BaseModel
from typing import Optional

class PaymentMethodType(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    CHEQUE = "CHEQUE"
    VOUCHER = "VOUCHER"

class PaymentMethodInputModel(BaseModel):
    method_type: PaymentMethodType 
    description: Optional[str | None] = None

class PaymentMethodOutputModel(BaseModel):
    payment_method_id: int
    method_type: PaymentMethodType 
    description: str