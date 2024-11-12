from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey, Index
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Enum as SAEnum
from datetime import date
import string
import secrets
import enum

if TYPE_CHECKING:
    from src.models.customers import Customers
    from src.models.visit_tickets import VisitTickets
    from src.models.ticket_types import TicketTypes

class TicketStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    USED = "USED"
    CANCELLED = "CANCELLED"


class Tickets(SQLModel, table=True):
    __tablename__ = "tickets"

    ticket_id: str = Field(
        default_factory=lambda: Tickets.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12),
            primary_key=True,
            nullable=False,
            comment="Unique identifier for each ticket"
        ),
        alias="TicketID"
    )
    
    customer_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("customers.customer_id"),
            nullable=False,
            comment="Foreign key linking the ticket to the customer who purchased it"
        ),
        alias="CustomerID"
    )
    
    ticket_type_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            ForeignKey("ticket_type.ticket_type_id"),
            nullable=False,
            comment="Foreign key linking to ticket_type table"
        ),
        alias="TicketTypeID"
    )
    
    price: float = Field(
        sa_column=Column(
            mysql.DECIMAL(10, 2),
            nullable=False,
            comment="The original price of the ticket"
        ),
        alias="Price"
    )
    
    purchase_date: date = Field(
        sa_column=Column(
            mysql.DATE,
            nullable=False,
            comment="The date when the ticket was purchased"
        ),
        alias="PurchaseDate"
    )
    
    start_date: date = Field(
        sa_column=Column(
            mysql.DATE,
            nullable=False,
            comment="The start date for the validity of the ticket"
        ),
        alias="StartDate"
    )
    
    expiration_date: date = Field(
        sa_column=Column(
            mysql.DATE,
            nullable=False,
            comment="The expiration date of the ticket"
        ),
        alias="ExpirationDate"
    )
    
    discount: float = Field(
        sa_column=Column(
            mysql.DECIMAL(4, 2),
            nullable=False,
            comment="The discount applied to the ticket price (percentage)"
        ),
        alias="Discount"
    )
    
    special_access: Optional[str] = Field(
        sa_column=Column(
            mysql.VARCHAR(45),
            nullable=True,
            comment="Any special access provided with the ticket (if available)"
        ),
        alias="SpecialAccess"
    )
    
    status: TicketStatus = Field(
        sa_column=Column(
            SAEnum(TicketStatus, values_callable=lambda x: [e.value for e in x]),
            nullable=False,
            default="ACTIVE",
            comment="The current status of the ticket (ACTIVE, EXPIRED, USED, CANCELLED)"
        ),
        alias="Status"
    )
    
    customer: "Customers" = Relationship(back_populates="tickets")
    visit_tickets: List["VisitTickets"] = Relationship(back_populates="ticket")
    ticket_type: "TicketTypes" = Relationship(back_populates="tickets")

    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount / 100), 2)

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    __table_args__ = (
        Index("idx_ticket_id", "ticket_id"),
        Index("idx_customer_id", "customer_id")
    )