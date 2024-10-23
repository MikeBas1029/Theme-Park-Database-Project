import string 
import secrets
import enum
from datetime import date
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
from sqlalchemy import Enum as SAEnum


if TYPE_CHECKING:
    from src.models.customers import Customers
    from src.models.visit_tickets import VisitTickets

# Enum for Ticket Status
class TicketStatus(str, enum.Enum):
    """
    Enumeration for the status of the ticket.
    """
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    USED = "USED"
    CANCELLED = "CANCELLED"

# Enum for Ticket Types
class TicketType(str, enum.Enum):
    """
    Enumeration for the different types of tickets available.
    """
    SEASONAL = "SEASONAL"
    WEEKEND = "WEEKEND"
    DAY_PASS = "DAY_PASS"
    VIP = "VIP"
    GROUP = "GROUP"
    STUDENT = "STUDENT"


class Tickets(SQLModel, table=True):
    """
    Represents a ticket purchased by a customer, with information such as the ticket type, 
    price, purchase date, and discount. This model also provides the calculated final price 
    after applying the discount.

    Attributes:
        ticket_id (int): Unique identifier for the ticket (Primary Key).
        customer_id (int): Foreign key linking the ticket to the customer who purchased it.
        ticket_type (TicketType): The type of the ticket (e.g., "VIP", "DAY_PASS").
        price (float): The original price of the ticket.
        purchase_date (date): The date when the ticket was purchased.
        start_date (date): The start date for the validity of the ticket.
        expiration_date (date): The expiration date of the ticket.
        discount (float): The discount applied to the ticket price (percentage).
        special_access (Optional[str]): Any special access provided with the ticket (if any).
        status (TicketStatus): The current status of the ticket (ACTIVE, EXPIRED, etc.).

    Relationships:
        customer (Customers): The customer who purchased the ticket.
        visit_tickets (List[VisitTickets]): The visits associated with this ticket through a many-to-many relationship.

    Derived Properties:
        final_price (float): The final price of the ticket after applying the discount.
    """
    
    __tablename__ = "tickets"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    

    ticket_id: str = Field(
        default=None,
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
    
    ticket_type: TicketType = Field(
        sa_column=Column(
            SAEnum(TicketType, values_callable=lambda x: [e.value for e in x]),  # Enum type for ticket type
            nullable=False,  
            comment="The type of the ticket (e.g., 'VIP', 'DAY_PASS')"  
        ), 
        alias="TicketType"
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
            mysql.DECIMAL(4, 2),  # Decimal type for discount percentage
            nullable=False,  
            comment="The discount applied to the ticket price (percentage)"  
        ), 
        alias="Discount"
    )
    
    special_access: Optional[str] = Field(
        sa_column=Column(
            mysql.VARCHAR(45),  # String type for special access details (if any)
            nullable=True,  
            comment="Any special access provided with the ticket (if available)"  
        ), 
        alias="SpecialAccess"
    )
    
    status: TicketStatus = Field(
        sa_column=Column(
            SAEnum(TicketStatus, values_callable=lambda x: [e.value for e in x]), # Enum type for ticket status (ACTIVE, EXPIRED, etc.)
            nullable=False,  
            default="ACTIVE",  
            comment="The current status of the ticket (ACTIVE, EXPIRED, USED, CANCELLED)"  
        ), 
        alias="Status"
    )
    
    # Relationships
    customer: "Customers" = Relationship(
        back_populates="tickets", 
    )

    # Many to many relationship with Visits through VisitTickets
    visit_tickets: List["VisitTickets"] = Relationship(
        back_populates="ticket", 
    )

    # Derived property for calculating final price after discount
    @property
    def final_price(self) -> float:
        """
        Calculate the final price of the ticket after applying the discount.

        The discount is applied as a percentage (e.g., if the discount is 20, the price 
        is reduced by 20%). The result is rounded to two decimal places for precision.

        Returns:
            float: The final price of the ticket after applying the discount.
        """
        return round(self.price * (1 - self.discount / 100), 2)
    
    __table_args__ = (
        Index("idx_ticket_id", "ticket_id"),  # Index for the ticket_id column
        Index("idx_customer_id", "customer_id")  # Index for the customer_id column
    )