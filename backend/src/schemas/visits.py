from typing import Optional
from datetime import date
from pydantic import BaseModel

class Visit(BaseModel):
    visit_id: str 
    customer_id: int
    visit_date: date
    visit_feedback: Optional[str]
    visit_rating: Optional[float]

class VisitCreateModel(BaseModel):
    customer_id: int
    visit_date: date

class VisitUpdateModel(BaseModel):
    customer_id: int
    visit_feedback: Optional[str | None] = None
    visit_rating: Optional[float | None] = None