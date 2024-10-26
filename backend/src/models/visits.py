import string
import secrets
from datetime import date
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

if TYPE_CHECKING:
    from src.models.customers import Customers
    from src.models.visit_tickets import VisitTickets


class Visits(SQLModel, table=True):
    """
    Represents a visit by a customer, including visit details such as the date, feedback, and rating.

    Attributes:
        visit_id (int): The unique identifier for the visit.
        customer_id (int): Foreign key referencing the customer who made the visit.
        visit_date (datetime): The date and time of the visit.
        visit_feedback (Optional[str]): The feedback left by the customer regarding the visit.
        visit_rating (Optional[float]): The rating given by the customer for the visit.

    Relationships:
        customer (Customers): The customer associated with the visit.
        visit_ticket (VisitTickets): The tickets associated with the visit.
    """

    __tablename__ = "visits"
    
    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    visit_id: str = Field(
        default_factory=lambda: Visits.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12), 
            nullable=False, 
            primary_key=True, 
            comment="The unique identifier for the visit"
        ),
        alias="VisitID"
    )
    
    customer_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12), 
            ForeignKey("customers.customer_id"), 
            nullable=False,
            comment="Foreign key referencing the customer who made the visit"
        ),  
        alias="CustomerID"
    )

    visit_date: date = Field(
        sa_column=Column(
            mysql.DATE, 
            nullable=False, 
            comment="The date and time of the visit"
        ), 
        alias="VisitDate"
    )
    
    visit_feedback: Optional[str] = Field(
        sa_column=Column(
            mysql.TEXT, 
            nullable=True, 
            comment="The feedback left by the customer regarding the visit"
        ),
        alias="VisitFeedback"
    )
    
    visit_rating: Optional[float] = Field(
        sa_column=Column(
            mysql.DECIMAL(2, 1), 
            nullable=True, 
            comment="The rating given by the customer for the visit"
        ),
        alias="VisitRating"
    )

    # Relationships with cascading behavior
    customer: "Customers" = Relationship(
        back_populates="visits"
    )
    
    visit_ticket: "VisitTickets" = Relationship(
        back_populates="visit", 
        cascade_delete=True,
    )

    __table_args__ = (
        Index("idx_customer_id", "customer_id"),
        Index("idx_visit_date", "visit_date")
    )