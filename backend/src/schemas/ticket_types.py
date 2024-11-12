from pydantic import BaseModel
from typing import Optional
from enum import Enum

# Enum for Ticket Types
class TicketType(str, Enum):
    SEASONAL = "SEASONAL"
    WEEKEND = "WEEKEND"
    DAY_PASS = "DAY_PASS"
    VIP = "VIP"
    GROUP = "GROUP"
    STUDENT = "STUDENT"


class TicketTypeOutputModel(BaseModel):
    ticket_type_id: int 
    ticket_type: TicketType 
    description: Optional[str]
    base_price: float 

class TicketTypeInputModel(BaseModel):
    ticket_type: TicketType 
    description: Optional[str]
    base_price: float 
