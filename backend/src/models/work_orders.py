from enum import Enum
from datetime import datetime, timezone
import sqlalchemy.dialects.mysql as mysql
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey

if TYPE_CHECKING:
    from src.models.rides import Rides
    from src.models.sections import Section
    from src.models.invoices import Invoice
    from src.models.employees import Employees


class MaintenanceType(str, Enum):
    REPAIR = "repair"
    INSPECTION = "inspection"
    UPGRADE = "upgrade"

class WorkOrderStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"

class WorkOrders(SQLModel, table=True):
    """
    Represents a work order for maintenance, which includes information on the section,
    ride, maintenance type, and worker assigned to the task.

    Attributes:
        woid (int): The unique identifier for the work order.
        section_id (int): Foreign key for the section where maintenance is carried out.
        ride_id (Optional[int]): Foreign key for the ride being serviced, if applicable.
        invoice_id (Optional[int]): Foreign key to an invoice related to the work order.
        maintenance_date (datetime): The date when maintenance is scheduled or completed.
        maintenance_type (str): The type of maintenance being performed (e.g., repair, inspection).
        assigned_worker_id (int): Foreign key for the employee assigned to the work order.
        date_created (datetime): The timestamp when the work order was created.
        updated_at (datetime): The timestamp when the work order was last updated.
        created_by (Optional[int]): Foreign key to the employee who created the work order.
        updated_by (Optional[int]): Foreign key to the employee who last updated the work order.
        status (str): The current status of the work order (e.g., pending, completed).
    """
    __tablename__ = "workorder"
    
    woid: int = Field(
        default=None, 
        sa_column=Column(
            mysql.INTEGER, 
            nullable=False, 
            primary_key=True, 
            autoincrement=True,
            comment="The unique identifier for the work order."
        ),
        alias="WOID"
    )
    
    section_id: int = Field(
        default=None, 
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("sections.section_id"),  
            nullable=False,
            comment="Foreign key to the section where maintenance is carried out."
        ),
        alias="SectionID"
    )
    
    ride_id: Optional[int] = Field(
        default=None, 
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("rides.ride_id"),
            nullable=True,
            comment="Foreign key to the ride being serviced, if applicable."
        ),  
        alias="RideID"
    )
    
    invoice_id: Optional[int] = Field(
        default=None, 
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("invoices.invoice_id"),
            nullable=True,
            comment="Foreign key to an invoice related to the work order."
        ),
        alias="InvoiceID"
    )
    
    maintenance_date: datetime = Field(
        default=None, 
        sa_column=Column(
            mysql.TIMESTAMP(), 
            nullable=False,
            comment="The date when maintenance is scheduled or completed."
        ),
        alias="MaintenanceDate"
    )
    
    maintenance_type: MaintenanceType = Field(
        default=None, 
        sa_column=Column(
            mysql.ENUM(MaintenanceType), 
            nullable=False,
            comment="The type of maintenance being performed (e.g., repair, inspection)."
        ),
        alias="MaintenanceType"
    )
    
    assigned_worker_id: int = Field(
        default=None, 
        sa_column=Column(
            mysql.INTEGER, 
            ForeignKey("employees.ssn"),
            nullable=False,
            comment="Foreign key to the employee assigned to the work order."
        ),
        alias="AssignedWorkerID"
    )
    
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            mysql.DATETIME, 
            nullable=False,
            comment="The timestamp when the work order was created."
        ),
        alias="DateCreated"
    )
    
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            mysql.DATETIME, 
            nullable=False,
            sa_column_kwargs={"onupdate": "CURRENT_TIMESTAMP"}, 
            comment="The timestamp when the work order was last updated."
        ),
        alias="UpdatedAt"
    )
    
    created_by: Optional[str] = Field(
        default=None, 
        sa_column=Column(
            mysql.VARCHAR(9),
            ForeignKey("employees.ssn"), 
            nullable=True,
            comment="Foreign key to the employee who created the work order."
        ),
        alias="CreatedBy"
    )
    
    updated_by: Optional[str] = Field(
        default=None, 
        sa_column=Column(
            mysql.VARCHAR(9),
            ForeignKey("employees.ssn"), 
            nullable=True,
            comment="Foreign key to the employee who last updated the work order."
        ),
        alias="UpdatedBy"
    )
    
    status: WorkOrderStatus = Field(
        default=None, 
        sa_column=Column(
            mysql.ENUM(WorkOrderStatus), 
            nullable=False,
            comment="The current status of the work order (e.g., pending, completed)."
        ),
        alias="Status"
    )
    
    # Relationships
    section: "Section" = Relationship(back_populates="work_orders")
    assigned_worker: "Employees" = Relationship(back_populates="work_orders")
    creator: "Employees" = Relationship(back_populates="work_orders")
    updater: "Employees" = Relationship(back_populates="work_orders")
    ride: Optional["Rides"] = Relationship(back_populates="work_orders")
    invoice: Optional["Invoice"] = Relationship(back_populates="work_orders")

    __table_args__ = (
        Index("idx_woid", "woid"),
        Index("idx_maintenance_date", "maintenance_date"),
        Index("idx_assigned_worker_id", "assigned_worker_id"),
        Index("idx_date_created", "date_created"),
        Index("idx_updated_by", "updated_by")
    )