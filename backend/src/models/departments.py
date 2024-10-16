from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import date
from typing import Optional, List
from src.models import Employees, Section

class Departments(SQLModel, table=True):
    __tablename__ = "departments"
    
    department_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="DepartmentID"
    )
    name: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="Name")
    manager_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="employees.SSN",
        alias="EmployeeID"
    )
    manager_start_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="ManagerStartDate")
    num_employees: int = Field(sa_column=Column(mysql.INTEGER, nullable=False), alias="NumEmployee")
    budget: float = Field(sa_column=Column(mysql.FLOAT, nullable=False), alias="Budget")
    department_role: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(45)), alias="DepartmentRole")

    # Relationships
    manager: "Employees" = Relationship(back_populates="departments")
    sections: List["Section"] = Relationship(back_populates="department")
