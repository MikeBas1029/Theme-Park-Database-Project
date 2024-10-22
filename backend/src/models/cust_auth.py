import uuid 
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey
from sqlalchemy import Enum as SAEnum
from pydantic import EmailStr

if TYPE_CHECKING:
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
    customer_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            mysql.INTEGER,
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
            mysql.VARCHAR, 
            nullable=False, 
            server_default="user",
            comment="Customer role in the database that sets permission levels.",
        )
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(mysql.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=datetime.now))

    # Relationship
    customer: Optional["Customers"] = Relationship(back_populates="cust_auth")

    def __repr__(self):
        return f"<Customer {self.username}>"