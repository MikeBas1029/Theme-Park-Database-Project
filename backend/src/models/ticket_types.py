from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from src.models.tickets import Tickets 

# Enum for Ticket Types
class TicketType(str, Enum):
    SEASONAL = "SEASONAL"
    WEEKEND = "WEEKEND"
    DAY_PASS = "DAY_PASS"
    VIP = "VIP"
    GROUP = "GROUP"
    STUDENT = "STUDENT"


class TicketTypes(SQLModel, table=True):
    __tablename__ = "ticket_type"

    ticket_type_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            primary_key=True,
            autoincrement=True,
            nullable=False,
            comment="Auto-incrementing ID for ticket types"
        )
    )

    ticket_type: TicketType = Field(
        sa_column=Column(
            mysql.VARCHAR(20),
            nullable=False,
            unique=True,
            comment="Type of the ticket (e.g., 'SEASONAL', 'VIP')"
        )
    )
    
    description: Optional[str] = Field(
        sa_column=Column(
            mysql.VARCHAR(255),
            nullable=True,
            comment="Description of the ticket type with details of its features"
        )
    )
    
    base_price: float = Field(
        sa_column=Column(
            mysql.DECIMAL(10, 2),
            nullable=False,
            comment="The base price of this ticket type"
        )
    )

    tickets: List["Tickets"] = Relationship(back_populates="ticket_type")

    def __repr__(self):
        return f"<TicketType {self.ticket_type} - ${self.base_price}>"