import enum
from typing import Optional
from datetime import date
from pydantic import BaseModel

class TicketStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    USED = "USED"
    CANCELLED = "CANCELLED"

class TicketCreateModel(BaseModel):
    customer_id: str
    price: float 
    purchase_date: date
    start_date: date 
    expiration_date: date
    discount: float 
    special_access: Optional[str | None] = None
    ticket_type_id: int

class TicketUpdateModel(BaseModel):
    customer_id: str
    price: float 
    purchase_date: date
    start_date: date 
    expiration_date: date
    discount: float 
    special_access: Optional[str]
    status: TicketStatus 
    ticket_type_id: int

class TicketOutputModel(BaseModel):
    ticket_id: str
    customer_id: str
    price: float 
    purchase_date: date
    start_date: date 
    expiration_date: date
    discount: float 
    special_access: Optional[str | None] = None
    status: TicketStatus 
    ticket_type_id: int