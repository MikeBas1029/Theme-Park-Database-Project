from datetime import datetime, timedelta
from typing import List, TYPE_CHECKING, Optional
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
from sqlalchemy import event, func, text
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression

if TYPE_CHECKING:
    from src.models.ride_type import RideType
    from src.models.ride_usage import RideUsage
    from src.models.sections import Section
    from src.models.work_orders import WorkOrders

# Custom SQL expression to get the current UTC timestamp
class UtcNow(expression.FunctionElement):
    type = mysql.TIMESTAMP()

@compiles(UtcNow, 'mysql')
def mysql_utc_now(element, compiler, **kw):
    return "UTC_TIMESTAMP()"

class Rides(SQLModel, table=True):
    """
    Represents a ride in the theme park, including the ride's details such as type, status, last inspection date, 
    and associated section and work order.
    """
    __tablename__ = "rides"  # Defines the name of the table in the database
    
    # ride_id is the primary key for the rides table, uniquely identifying each ride.
    ride_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True),
        alias="RideID"
    )
    
    # section_id is a foreign key that links each ride to a section of the park where it is located.
    section_id: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, ForeignKey("sections.section_id"), nullable=False),
        alias="SectionID"
    )
    
    # The name of the ride (e.g., "Roller Coaster", "Ferris Wheel").
    name: str = Field(
        default=None,
        sa_column=Column(mysql.VARCHAR(50), nullable=False),
        alias="Name"
    )
    
    # ride_type references the type of ride, which is a foreign key from the ride_type table.
    ride_type: int = Field(
        default=None,
        sa_column=Column(mysql.TINYINT(), ForeignKey("ride_type.ride_type_id"), nullable=False),
        alias="RideType"
    )
    
    # The date and time of the last inspection. The ride must be inspected periodically for safety.
    last_inspected: Optional[datetime] = Field(
        default=None,
        sa_column=Column(mysql.TIMESTAMP(), default=None, nullable=True),
        alias="LastInspected"
    )
    
    # # work order ID (WOID) is a foreign key linking this ride to a specific work order (maintenance task).
    # woid: Optional[int] = Field(
    #     default=None,
    #     sa_column=Column(mysql.INTEGER, ForeignKey("workorder.woid"), nullable=True),
    #     alias="WOID"
    # )
    
    # The height requirement (in cm) to go on the ride. This ensures safety by restricting access to certain rides.
    height_requirement: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, nullable=False, comment="Height required to go on the ride."),
        alias="HeightRequirement"
    )
    
    # The ride capacity, i.e., how many people the ride can accommodate at once.
    capacity: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="Capacity"
    )
    
    # The current status of the ride, which can be one of the following: 
    # "OPEN", "CLOSED - MAINTENANCE", or "CLOSED - RAINOUT".
    status: str = Field(
        default=None,  
        sa_column=Column(mysql.ENUM("OPEN", "CLOSED - MAINTENANCE", "CLOSED - RAINOUT"), nullable=False, 
                         comment="The state of the ride: OPEN, CLOSED - Maintenance, CLOSED - RainOut."),
        alias="Status"
    )
    
    # Relationships
    # The `ride_type_rel` relationship links each ride to its type (from the RideType table).
    ride_type_rel: "RideType" = Relationship(back_populates="rides", sa_relationship_kwargs={"lazy": "joined"})
    
    # The `work_order` relationship links each ride to its maintenance work order (from the WorkOrders table).
    work_order: List["WorkOrders"] = Relationship(
        back_populates="ride", 
        cascade_delete=True,
    )
    
    # The `section` relationship links each ride to a section in the park where the ride is located (from the Section table).
    section: "Section" = Relationship(back_populates="rides")
    
    # The `ride_usages` relationship links each ride to instances of its usage by customers (from the RideUsage table).
    ride_usages: List["RideUsage"] = Relationship(back_populates="ride")

    # Table arguments to define additional properties like indexes.
    __table_args__ = (
        Index("idx_ride_id", "ride_id"),  # Index for faster queries by ride ID
    )

# Event listener to check the last inspection date and update the ride status before insert or update
@event.listens_for(Rides, 'before_update')
@event.listens_for(Rides, 'before_insert')
def check_last_inspected(mapper, connection, target):
    """
    This event listener is triggered before a ride record is inserted or updated in the database.
    If the ride's last inspection date is more than 7 days ago, it updates the ride's status to "CLOSED - MAINTENANCE",
    unless the ride is already in maintenance.
    """
    if target.last_inspected:
        # Calculate the number of days since the last inspection.
        days_since_inspection = (func.utc_timestamp() - target.last_inspected).days
        # If the inspection is overdue by more than 7 days, set the status to "CLOSED - MAINTENANCE".
        if days_since_inspection > 7 and target.status != "CLOSED - MAINTENANCE":
            target.status = "CLOSED - MAINTENANCE"
