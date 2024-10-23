import string 
import secrets
import enum 
from datetime import date, timedelta
from typing import List, TYPE_CHECKING, Optional
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
from sqlalchemy import event, Enum as SAEnum

if TYPE_CHECKING:
    from src.models.ride_type import RideType
    from src.models.ride_usage import RideUsage
    from src.models.sections import Section
    from src.models.work_orders import WorkOrders

class RideStatus(str, enum.Enum):
    open = "OPEN"
    closed_maint = "CLOSED(M)"
    closed_rainout = "CLOSED(R)"

class Rides(SQLModel, table=True):
    """
    Represents a ride in the theme park, including the ride's details such as type, status, last inspection date, 
    and associated section and work order.
    """
    __tablename__ = "rides"  # Defines the name of the table in the database


    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    

    # ride_id is the primary key for the rides table, uniquely identifying each ride.
    ride_id: str = Field(
        default_factory=lambda: Rides.generate_random_id(),
        sa_column=Column(mysql.VARCHAR(12), nullable=False, primary_key=True),
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
    last_inspected: Optional[date] = Field(
        default=None,
        sa_column=Column(mysql.DATE(), default=None, nullable=True),
        alias="LastInspected"
    )
    
    # The height requirement (in inches) to go on the ride. This ensures safety by restricting access to certain rides.
    height_requirement: int = Field(
        default=None,
        sa_column=Column(mysql.INTEGER, nullable=False, comment="Height required to go on the ride in inches."),
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
    status: RideStatus = Field(
        default=None,  
        sa_column=Column(
            SAEnum(RideStatus, values_callable=lambda x: [e.value for e in x]), 
            nullable=False, 
            comment="The state of the ride: OPEN, CLOSED(M), CLOSED(RO)"),
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
    If the ride's last inspection date is more than 7 days ago, it updates the ride's status to "CLOSED(M)",
    unless the ride is already in maintenance.
    """
    if target.last_inspected:
        # Calculate the date 7 days ago
        seven_days_ago = date.today() - timedelta(days=7)
        
        # If the last inspection was more than 7 days ago, set the status to "CLOSED(M)"
        if target.last_inspected < seven_days_ago and target.status != RideStatus.closed_maint:
            target.status = RideStatus.closed_maint