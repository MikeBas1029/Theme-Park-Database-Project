from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.departments import Departments

class DepartmentRoles(SQLModel, table=True):
    __tablename__ = "deparmentroles"
    
    # department_role_id is the primary key that uniquely identifies each department role.
    department_role_id: int = Field(
        sa_column=Column(mysql.INTEGER, primary_key=True, nullable=False, comment="Unique ID for each department role"),
        alias="DepartmentRoleID"
    )
    
    # department_id is the foreign key linking the department role to a specific department.
    # It refers to the `DepartmentID` in the `departments` table.
    department_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("departments.department_id"), nullable=False, comment="Department ID this role belongs to"),
        alias="DepartmentID"
    )
    
    # role_description provides a description of the specific role within the department.
    # It’s a string that is required for each role.
    role_description: str = Field(sa_column=Column(mysql.VARCHAR(200), nullable=False, comment="Description of the department role"), alias="RoleDescription")

    # Relationships
    # A department role is associated with one department, represented here by the `department` relationship.
    department: "Departments" = Relationship(back_populates="department_roles")

    # Table index: Adds an index on the department_role_id field.
    # This improves performance when querying by department_role_id.
    __table_args__ = (
        Index("idx_department_role_id", "department_role_id"),
    )