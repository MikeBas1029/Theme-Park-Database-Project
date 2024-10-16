from datetime import date, time
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Section

class Entertainment(SQLModel, table=True):
    __tablename__ = "entertainment"
    
    show_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="ShowID"
    )
    section_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="sections.SectionID",
        alias="SectionID"
    )
    show_name: str = Field(sa_column=Column(mysql.VARCHAR(45), nullable=False), alias="ShowName")
    show_date: date = Field(sa_column=Column(mysql.DATE, nullable=False), alias="ShowDate")
    show_time: time = Field(sa_column=Column(mysql.TIME, nullable=False), alias="ShowTime")
    capacity: int = Field(sa_column=Column(mysql.INTEGER, nullable=False), alias="Capacity")
    ticket_price: float = Field(sa_column=Column(mysql.FLOAT, nullable=False), alias="TicketPrice")
    status: str = Field(
        sa_column=Column(mysql.ENUM("ACTIVE", "CANCELED", "POSTPONED"), nullable=False),
        alias="Status"
    )

    # Relationships
    section: "Section" = Relationship(back_populates="entertainment")
