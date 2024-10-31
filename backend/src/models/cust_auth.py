import uuid 
from sqlalchemy import event
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import Enum as SAEnum
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey, select

from src.models.customers import Customers

class CustAuth(SQLModel, table=True):
    __tablename__ = "customer_auth"
    uid: uuid.UUID = Field(
        sa_column=Column(
            mysql.VARCHAR(36), 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4)
    )
    customer_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("customers.customer_id", ondelete="SET NULL"),
            nullable=True,
            comment="Foreign key to Customers table, some customers may have user accounts"
        )
    )
    
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(
            mysql.VARCHAR(4), 
            nullable=False, 
            server_default="user",
            comment="Customer role in the database that sets permission levels.",
        )
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(mysql.VARCHAR(60), nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=datetime.now))

    # Relationship
    customer: Optional["Customers"] = Relationship(back_populates="cust_auth")

    def __repr__(self):
        return f"<Customer {self.username}>"
    
@event.listens_for(CustAuth, "before_insert")
def set_unit_price(mapper, connection, target):
    # Use a regular session with a synchronous query
    with Session(connection) as session:
        result = session.execute(
            select(Customers).where(Customers.email == target.email)
        )
        cust = result.scalar_one_or_none()
        if cust:
            target.customer_id = cust.customer_id
