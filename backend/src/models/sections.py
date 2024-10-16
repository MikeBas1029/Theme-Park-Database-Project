from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from typing import List
from src.models import Departments, Rides, Shops, Restaurants, Entertainment

class Section(SQLModel, table=True):
    __tablename__ = "sections"
    
    section_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="SectionID"
    )
    department_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="departments.DepartmentID",
        alias="DepartmentID"
    )
    location: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="Location")
    name: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="Name")
    lot_size: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="LotSize")

    # Relationships
    department: "Departments" = Relationship(back_populates="sections")
    rides: List["Rides"] = Relationship(back_populates="section")
    shops: List["Shops"] = Relationship(back_populates="park_section")
    restaurants: List["Restaurants"] = Relationship(back_populates="park_section")
    entertainment: List["Entertainment"] = Relationship(back_populates="section")