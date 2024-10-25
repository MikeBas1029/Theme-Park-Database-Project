import string 
import secrets
from datetime import date
import sqlalchemy.dialects.mysql as mysql
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

if TYPE_CHECKING:
    from src.models.customers import Customers
    from src.models.sales_order_details import SalesOrderDetail

class SalesOrders(SQLModel, table=True):
    """
    Represents a sales order in the system, linking to a customer and containing details about the items purchased.
    
    Attributes:
        transaction_id (int): Unique identifier for the sales order (Primary Key).
        customer_id (int): Foreign key linking to the customer who placed the order.
        order_date (datetime): Timestamp indicating when the order was placed.
    
    Relationships:
        customer (Customers): Reference to the customer who placed the order.
        sales_order_details (List[SalesOrderDetail]): List of items included in the order, each with a quantity and price.
    
    Derived Property:
        total_amount (float): The total cost of the order, calculated as the sum of all details' subtotals.
    """
    
    __tablename__ = "sales_orders"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    # Primary key for the sales order
    transaction_id: str = Field(
        default_factory=lambda: SalesOrders.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12),
            nullable=False,
            primary_key=True,
            comment="Unique identifier for each sales order",
        ),
        alias="TransactionID"
    )
    
    customer_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("customers.customer_id"),  # Foreign key linking to the Customers table
            nullable=False,
            comment="Foreign key linking to Customers",
        ),
        alias="CustomerID"
    )

    order_date: date = Field(
        sa_column=Column(
            mysql.DATE,
            nullable=False,
            comment="Order timestamp including both date and time"
        ),
        alias="OrderDate"
    )
    detail_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("sales_order_details.detail_id"),  # Foreign key to sales order table
            nullable=False,
            comment="Foreign key referencing the sales order",
        ),
        alias="TransactionID"
    )
    
    # Relationships to other models
    customer: "Customers" = Relationship(back_populates="sales_orders")  # Relationship with the Customers table
    sales_order_details: List["SalesOrderDetail"] = Relationship(
        back_populates="sales_order",  # Relationship with the SalesOrderDetail table
    )

    # Derived property for calculating the total order amount
    @property
    def total_amount(self) -> float:
        """
        Calculate the total cost of the sales order.
        
        This is the sum of the subtotals of all items in the order, 
        which are calculated as quantity * unit price.
        
        Returns:
            float: The total amount of the sales order, rounded to two decimal places.
        """
        # Sum the subtotals of all the sales order details and round to two decimal places
        return round(sum(detail.quantity * detail.unit_price for detail in self.sales_order_details), 2)
    
    # Table-level constraints and indexes
    __table_args__ = (
        Index("idx_customer_id", "customer_id"),  # Index on customer_id for faster lookups by customer
        Index("idx_transaction_id", "transaction_id")  # Index on transaction_id for faster lookups by transaction
    )