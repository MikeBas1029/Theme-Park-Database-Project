import string
import secrets
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
    
    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    visit_ticket_id: str = Field(
        default_factory=lambda: VisitTickets.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12), 
            primary_key=True, 
            nullable=False,
            comment="The unique identifier for the visit"
        ),
        alias="VisitID"
    )
    
    visit_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12), 
            ForeignKey("visits.visit_id"), 
            nullable=False,
            comment="Foreign key for the visit"
        ),
        alias="VisitID"
    )
    
    ticket_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12), 
            ForeignKey("tickets.ticket_id"), 
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
        back_populates="visit_ticket"
    )
    
    ticket: "Tickets" = Relationship(
        back_populates="visit_tickets"
    )