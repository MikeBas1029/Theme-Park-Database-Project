from datetime import date, time
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.sections import Section

class Entertainment(SQLModel, table=True):
    __tablename__ = "entertainment"
    
    # ShowID is the primary key for the entertainment shows table.
    # It uniquely identifies each show in the system.
    show_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True, comment="Unique identifier for each show (primary key)"),
        alias="ShowID"
    )
    
    # SectionID is a foreign key referencing the 'sections' table.
    # It links each show to a specific section within the venue.
    section_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("sections.section_id"), nullable=False, comment="Foreign key linking to the SectionID in the sections table"),
        alias="SectionID"
    )

    # ShowName is the name of the entertainment show.
    # It is a required field, typically a string of the show's title.
    show_name: str = Field(
        sa_column=Column(mysql.VARCHAR(45), nullable=False, comment="Name of the show"),
        alias="ShowName"
    )

    # ShowDate represents the date when the show will take place.
    # This is a required field and is stored as a date value.
    show_date: date = Field(
        sa_column=Column(mysql.DATE, nullable=False, comment="Date the show is scheduled"),
        alias="ShowDate"
    )

    # ShowTime represents the time when the show will begin.
    # This is a required field and is stored as a time value.
    show_time: time = Field(
        sa_column=Column(mysql.TIME, nullable=False, comment="Time the show is scheduled to start"),
        alias="ShowTime"
    )

    # Capacity indicates the number of seats available for the show.
    # It is a required field, stored as an integer value.
    capacity: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False, comment="Capacity or number of seats for the show"),
        alias="Capacity"
    )

    # TicketPrice indicates the price of a ticket for the show.
    # It is a required field, stored as a floating-point number.
    ticket_price: float = Field(
        sa_column=Column(mysql.FLOAT, nullable=False, comment="Price of a ticket for the show"),
        alias="TicketPrice"
    )

    # Status indicates the current status of the show.
    # It can be either 'ACTIVE', 'CANCELED', or 'POSTPONED' as defined in the ENUM.
    status: str = Field(
        sa_column=Column(mysql.ENUM("ACTIVE", "CANCELED", "POSTPONED"), nullable=False, comment="Status of the show (e.g., ACTIVE, CANCELED, POSTPONED)"),
        alias="Status"
    )

    # Relationships
    # Establishes a relationship with the Section model.
    # The "section" field is populated with the related section based on section_id.
    section: "Section" = Relationship(back_populates="entertainment")

    # Table index: Adds an index on the show_id field.
    # This index improves performance for queries filtering by show_id.
    __table_args__ = (
        Index("idx_show_id", "show_id"),
    )