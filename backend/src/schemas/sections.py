from typing import Optional
from pydantic import BaseModel

class Section(BaseModel):
    section_id: int
    department_id: int
    location: str
    name: str 
    lot_size: str

class SectionCreateModel(BaseModel):
    department_id: int
    location: str
    name: str 
    lot_size: str

class SectionUpdateModel(BaseModel):
    department_id: int
    location: Optional[str]
    name: Optional[str] 
    lot_size: Optional[str]
