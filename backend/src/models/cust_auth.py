import uuid 
import string
import secrets
from typing import Optional
from sqlalchemy import event
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import Enum as SAEnum
import sqlalchemy.dialects.mysql as mysql
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

def generate_random_id(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))   

@event.listens_for(CustAuth, "before_insert")
def lookup_customer_id(mapper, connection, target):
    # Use a regular session with a synchronous query
    with Session(connection) as session:
        result = session.execute(
            select(Customers).where(Customers.email == target.email)
        )
        cust = result.scalar_one_or_none()
        if cust:
            target.customer_id = cust.customer_id
        else:
            # if customer does not exist, create new Customer record
            customer_id = generate_random_id()
            new_customer = Customers(
                customer_id=customer_id,
                first_name=target.first_name,
                last_name=target.last_name,
                email=target.email,
                phone_number="-",
                country="US",
                membership_type="Bronze",
                registration_date=datetime.now().date()
            )

            # Add and commit new user
            session.add(new_customer)
            session.commit()
            session.refresh(new_customer)

            # Assign the new customer id to cust auth
            target.customer_id = customer_id
