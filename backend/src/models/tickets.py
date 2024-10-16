from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List
import sqlalchemy.dialects.mysql as mysql
from datetime import date
from enum import Enum
from src.models import Customers, VisitTickets

# Enum for Ticket Status
class TicketStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    USED = "USED"
    CANCELLED = "CANCELLED"

# Enum for Ticket Types
class TicketType(str, Enum):
    SEASONAL = "SEASONAL"
    WEEKEND = "WEEKEND"
    DAY_PASS = "DAY_PASS"
    VIP = "VIP"
    GROUP = "GROUP"
    STUDENT = "STUDENT"


class Tickets(SQLModel, table=True):
    __tablename__ = "tickets"
    
    ticket_id: int = Field(
        default=None,
        primary_key=True,
        index=True,
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="TicketID"
    )
    
    customer_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="customers.CustomerID",
        alias="CustomerID"
    )
    
    ticket_type: TicketType = Field(sa_column=Column(mysql.ENUM(TicketType), nullable=False), alias="TicketType")
    
    # Price field using DECIMAL for precision
    price: float = Field(sa_column=Column(mysql.DECIMAL(10, 2), nullable=False), alias="Price")
    
    purchase_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="PurchaseDate")
    
    start_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="StartDate")
    
    expiration_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="ExpirationDate")
    
    # Discount field using DECIMAL for consistency with price
    discount: float = Field(sa_column=Column(mysql.DECIMAL(4, 2), nullable=False), alias="Discount")
    
    # Special access field is optional
    special_access: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(45)), alias="SpecialAccess")
    
    # Status field with default value set to 'ACTIVE'
    status: TicketStatus = Field(sa_column=Column(mysql.ENUM(TicketStatus), nullable=False, default="ACTIVE"), alias="Status")
    
    
    # Relationships
    customer: "Customers" = Relationship(back_populates="tickets", cascade_delete=True)

    # Many to many relationship with Visits through VisitTickets
    visit_tickets: List["VisitTickets"] = Relationship(back_populates="ticket", cascade_delete=True)

    # Derived property for calculating final price after discount
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount / 100), 2)
    