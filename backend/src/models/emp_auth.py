import uuid 
import enum
from typing import Optional
from sqlalchemy import event
from datetime import datetime
from sqlalchemy.orm import Session
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey, select
from sqlalchemy import Enum as SAEnum
from pydantic import EmailStr

from src.models.employees import Employees

class EmpRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class EmpAuth(SQLModel, table=True):
    __tablename__ = "employee_auth"
    uid: uuid.UUID = Field(
        sa_column=Column(
            mysql.VARCHAR(36), 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4)
    )

    employee_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            mysql.VARCHAR(8),
            ForeignKey("employees.employee_id", ondelete="SET NULL"),
            nullable=True,
            comment="Foreign key to employees table, may be optional"
        )
    )
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: EmpRole = Field(
        default="employee",
        sa_column=Column(
            SAEnum(EmpRole, values_callable=lambda x: [e.value for e in x]), 
            nullable=False, 
            comment="Employee role in the database that sets permission levels.",
        )
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(mysql.VARCHAR(60), nullable=False), exclude=True
    )
    password_on_create: Optional[str] 
    created_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(mysql.TIMESTAMP, default=datetime.now))

    # Relationship 
    employee: Optional["Employees"] = Relationship(back_populates="emp_auth")

    def __repr__(self):
        return f"<Employee {self.username}>"
    

@event.listens_for(EmpAuth, "before_insert")
def set_unit_price(mapper, connection, target):
    # Use a regular session with a synchronous query
    with Session(connection) as session:
        result = session.execute(
            select(Employees).where(Employees.email == target.email)
        )
        employee = result.scalar_one_or_none()
        if employee:
            target.customer_id = employee.customer_id
