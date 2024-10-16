from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import datetime
from typing import Optional, List
from src.models import Rides, Section, Invoice

class WorkOrder(SQLModel, table=True):
    __tablename__ = "workorder"
    
    woid: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="WOID"
    )
    
    section_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="sections.SectionID",  # Foreign key to the sections table
        alias="SectionID"
    )
    
    ride_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=True),  # Foreign key to the rides table
        foreign_key="rides.RideID",
        alias="RideID"
    )
    
    invoice_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="invoices.InvoiceID",
        alias="InvoiceID"
    )
    
    maintenance_date: datetime = Field(
        default=None, 
        sa_column=Column(mysql.TIMESTAMP(), nullable=False),
        alias="MaintenanceDate"
    )
    
    maintenance_type: Optional[str] = Field(
        default=None, 
        sa_column=Column(mysql.VARCHAR(25), nullable=False),
        alias="MaintenanceType"
    )
    
    assigned_work_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="AssignedWorkID"
    )
    
    date_created: datetime = Field(
        default=None, 
        sa_column=Column(mysql.DATE(), nullable=False),
        alias="DateCreated"
    )
    
    status: str = Field(
        default=None, 
        sa_column=Column(mysql.VARCHAR(25), nullable=False),
        alias="Status"
    )
    
    # Relationships
    section: "Section" = Relationship(back_populates="work_orders")
    ride: Optional["Rides"] = Relationship(back_populates="work_orders")
    invoice: Optional["Invoice"] = Relationship(back_populates="work_orders")