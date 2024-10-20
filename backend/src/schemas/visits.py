from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class VisitOutputModel(BaseModel):
    visit_id: int 
    customer_id: int
    visit_date: datetime
    visit_feedback: Optional[str]
    visit_rating: Optional[float]

class VisitInputModel(BaseModel):
    customer_id: int
    visit_date: datetime
    visit_feedback: Optional[str]
    visit_rating: Optional[float]