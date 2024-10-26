from pydantic import BaseModel

class VisitTicketOutputModel(BaseModel):
    visit_ticket_id: str
    visit_id: str 
    ticket_id: str
    ticket_count: int

class VisitTicketInputModel(BaseModel):
    visit_id: str 
    ticket_id: str
    ticket_count: int