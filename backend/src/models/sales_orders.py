from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import datetime
from typing import Optional, List
from src.models import Customers, SalesOrderDetail

class SalesOrders(SQLModel, table=True):
    __tablename__ = "sales_orders"

    # Primary key
    transaction_id: int = Field(
        primary_key=True,
        sa_column=Column(
            mysql.INTEGER,
            autoincrement=True,
            nullable=False,
            comment="Unique identifier for each sales order",
            index=True  
        ),
        alias="TransactionID"
    )
    
    customer_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            nullable=False,
            comment="Foreign key linking to Customers",
            index=True,  
            foreign_key="customers.CustomerID"  
        ),
        alias="CustomerID"
    )

    order_date: datetime = Field(
        sa_column=Column(
            mysql.DATETIME,
            nullable=False,
            index=True,  
            comment="Order timestamp including both date and time"
        ),
        alias="OrderDate"
    )
    
    # Relationships
    customer: "Customers" = Relationship(back_populates="sales_orders")
    sales_order_details: List["SalesOrderDetail"] = Relationship(
        back_populates="sales_order", 
        cascade_delete=True,  # Cascade delete for orphaned details
        comment="Link to associated sales order details"
    )

    @property
    def total_amount(self) -> float:
        """Calculate the total cost of the order as the sum of all details' subtotals."""
        return round(sum(detail.quantity * detail.unit_price for detail in self.sales_order_details), 2)