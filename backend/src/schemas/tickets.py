import enum
from typing import Optional
from datetime import date
from pydantic import BaseModel

class TicketStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    USED = "USED"
    CANCELLED = "CANCELLED"

class TicketType(str, enum.Enum):
    SEASONAL = "SEASONAL"
    WEEKEND = "WEEKEND"
    DAY_PASS = "DAY_PASS"
    VIP = "VIP"
    GROUP = "GROUP"
    STUDENT = "STUDENT"

class TicketCreateModel(BaseModel):
    customer_id: str
    ticket_type: TicketType
    price: float 
    purchase_date: date
    start_date: date 
    expiration_date: date
    discount: float 
    special_access: Optional[str | None] = None

class TicketUpdateModel(BaseModel):
    customer_id: str
    ticket_type: TicketType
    price: float 
    purchase_date: date
    start_date: date 
    expiration_date: date
    discount: float 
    special_access: Optional[str]
    status: TicketStatus 

class TicketOutputModel(BaseModel):
    ticket_id: str
    customer_id: str
    ticket_type: TicketType
    price: float 
    purchase_date: date
    start_date: date 
    expiration_date: date
    discount: float 
    special_access: Optional[str | None] = None
    status: TicketStatus 