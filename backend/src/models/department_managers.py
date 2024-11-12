from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey
import sqlalchemy.dialects.mysql as mysql
from typing import TYPE_CHECKING
import sqlalchemy as sa 
from datetime import date

if TYPE_CHECKING:
    from src.models.employees import Employees
    from src.models.departments import Departments


class DepartmentManagers(SQLModel, table=True):
    __tablename__ = "department_managers"

    department_id: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            ForeignKey("departments.department_id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
            comment="ID of the department"
        ),
        alias="DepartmentID"
    )

    employee_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(8),
            ForeignKey("employees.employee_id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
            comment="ID of the employee managing the department"
        ),
        alias="EmployeeID"
    )

    # manager_start_date represents the date when the manager started managing this department.
    manager_start_date: date = Field(sa_column=Column(mysql.DATE, nullable=False, comment="Start date of the department manager"), alias="ManagerStartDate")
    

    # Relationships to connect back to departments and employees
    department: "Departments" = Relationship(back_populates="manager")
    manager: "Employees" = Relationship(back_populates="managed_department")

        # Composite primary key definition
    __table_args__ = (
        sa.PrimaryKeyConstraint("department_id", "employee_id"),
    )