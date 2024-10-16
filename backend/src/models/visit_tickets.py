from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.model import Visits, Tickets

class VisitTickets(SQLModel, table=True):
    __tablename__ = "visit_tickets"

    visit_id: int = Field(
        primary_key=True,
        foreign_key="visits.VisitID",
        sa_column=Column(mysql.INTEGER, nullable=False)
    )
    ticket_id: int = Field(
        primary_key=True,
        foreign_key="tickets.TicketID",
        sa_column=Column(mysql.INTEGER, nullable=False)
    )
    
    # Optional: You could also track other attributes in this table
    ticket_count: int = Field(sa_column=Column(mysql.INTEGER, nullable=False, default=1))

    # Relationships
    visit: "Visits" = Relationship(back_populates="visit_tickets")
    ticket: "Tickets" = Relationship(back_populates="visit_tickets")