from datetime import date
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.employees import Employees
    from src.models.sections import Section
    from src.models.department_roles import DepartmentRoles

class Departments(SQLModel, table=True):
    __tablename__ = "departments"
    
    # department_id is the primary key that uniquely identifies each department.
    # It is an auto-incrementing integer.
    department_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True, comment="Unique ID for each department"),
        alias="DepartmentID"
    )
    
    # name is the name of the department, such as 'HR', 'Engineering', etc.
    # This field is required and stored as a string.
    name: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False, comment="Department name"), alias="Name")
    
    # manager_id is the foreign key that links to the employee managing this department.
    # It refers to the SSN of the employee in the employees table.
    manager_id: str = Field(
        sa_column=Column(mysql.VARCHAR(9), ForeignKey("employees.employee_id"), nullable=False, comment="ID of the manager for this department"),
        alias="EmployeeID"
    )
    
    # manager_start_date represents the date when the manager started managing this department.
    manager_start_date: date = Field(sa_column=Column(mysql.DATE, nullable=False, comment="Start date of the department manager"), alias="ManagerStartDate")
    
    # num_employees is the total number of employees in the department.
    num_employees: int = Field(sa_column=Column(mysql.INTEGER, nullable=False, comment="Number of employees in the department"), alias="NumEmployee")
    
    # budget is the total budget allocated to the department.
    # This field is required and stored as a float.
    budget: float = Field(sa_column=Column(mysql.FLOAT, nullable=False, comment="Budget allocated to the department"), alias="Budget")
    
    # department_role is an optional field describing the department's role or focus.
    # This can be used for additional context about the department.
    department_role: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(45), comment="Role or focus of the department"), alias="DepartmentRole")

    # Relationships
    # A department is managed by one employee, represented here as the `manager`.
    manager: "Employees" = Relationship(back_populates="departments")
    
    # A department can have multiple sections, represented as a list of `Section` objects.
    sections: List["Section"] = Relationship(back_populates="department")

    department_roles: List["DepartmentRoles"] = Relationship(back_populates="department") 

    # Table index: Adds an index on the department_id field.
    # This index improves performance for queries filtering by the department_id.
    __table_args__ = (
        Index("idx_department_id", "department_id"),
    )