from datetime import datetime
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

    # Primary key for the sales order
    transaction_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            autoincrement=True,
            nullable=False,
            primary_key=True,
            comment="Unique identifier for each sales order",
        ),
        alias="TransactionID"
    )
    
    customer_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            ForeignKey("customers.customer_id"),  # Foreign key linking to the Customers table
            nullable=False,
            comment="Foreign key linking to Customers",
        ),
        alias="CustomerID"
    )

    order_date: datetime = Field(
        sa_column=Column(
            mysql.DATETIME,
            nullable=False,
            comment="Order timestamp including both date and time"
        ),
        alias="OrderDate"
    )
    
    # Relationships to other models
    customer: "Customers" = Relationship(back_populates="sales_orders")  # Relationship with the Customers table
    sales_order_details: List["SalesOrderDetail"] = Relationship(
        back_populates="sales_order",  # Relationship with the SalesOrderDetail table
        cascade_delete=True,  # Cascade delete to remove orphaned sales order details when the sales order is deleted
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