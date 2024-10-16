from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import ForeignKeyConstraint
from datetime import datetime
from typing import Optional
from src.models import Customers, VisitTickets

class Visits(SQLModel, table=True):
    __tablename__ = "visits"
    
    visit_id: int = Field(
        default=None,
        primary_key=True,
        index=True,
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="VisitID"
    )
    customer_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=True, index=True),  # Add index for better performance
        foreign_key="customers.CustomerID",
        ondelete='SET NULL',
        alias="CustomerID"
    )

    visit_date: datetime = Field(sa_column=Column(mysql.DATE, nullable=False), alias="VisitDate")
    visit_feedback: Optional[str] = Field(sa_column=Column(mysql.TEXT, nullable=True), alias="VisitFeedback")
    visit_rating: Optional[float] = Field(sa_column=Column(mysql.DECIMAL(2, 1), nullable=True), alias="VisitRating")

    # Relationships with cascading behavior
    customer: "Customers" = Relationship(back_populates="visits")
    visit_ticket: "VisitTickets" = Relationship(back_populates="visits", cascade_delete=True)
