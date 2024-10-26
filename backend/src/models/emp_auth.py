import uuid 
import enum
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Column, Relationship, ForeignKey
from sqlalchemy import Enum as SAEnum
from pydantic import EmailStr

if TYPE_CHECKING:
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
            mysql.VARCHAR(7),
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