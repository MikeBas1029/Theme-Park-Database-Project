from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey
import sqlalchemy.dialects.mysql as mysql
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.visits import Visits
    from src.models.tickets import Tickets


class VisitTickets(SQLModel, table=True):
    """
    Represents the many-to-many relationship between visits and tickets in the system.

    Attributes:
        visit_id (int): The unique identifier for the visit.
        ticket_id (int): The unique identifier for the ticket.
        ticket_count (int): The number of tickets associated with the visit.

    Relationships:
        visit (Visits): The visit associated with the ticket.
        ticket (Tickets): The ticket associated with the visit.
    """

    __tablename__ = "visit_tickets"

    visit_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("visits.VisitID"), 
            primary_key=True, 
            nullable=False,
            comment="The unique identifier for the visit"
        ),
        alias="VisitID"
    )
    
    ticket_id: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("tickets.TicketID"), 
            primary_key=True, 
            nullable=False,
            comment="The unique identifier for the ticket"
        ),
        alias="TicketID"
    )
    
    ticket_count: int = Field(
        sa_column=Column(
            mysql.INTEGER, 
            nullable=False, 
            default=1,
            comment="The number of tickets associated with the visit"
        )
    )

    # Relationships
    visit: "Visits" = Relationship(
        back_populates="visit_tickets"
    )
    
    ticket: "Tickets" = Relationship(
        back_populates="visit_tickets"
    )