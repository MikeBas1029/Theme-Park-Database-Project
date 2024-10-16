from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Departments

class DepartmentRoles(SQLModel, table=True):
    __tablename__ = "deparmentroles"
    
    department_role_id: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="DepartmentRoleID"
    )
    department_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="departments.DepartmentID",
        alias="DepartmentID"
    )
    role_description: str = Field(sa_column=Column(mysql.VARCHAR(200), nullable=False), alias="RoleDescription")

    # Relationships
    department: "Departments" = Relationship(back_populates="department_roles")
