from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Items


class Merchandise(SQLModel, table=True):
    __tablename__ = "merchandise"
    
    merchandise_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="MerchandiseID"
    )
    item_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="items.SKU",
        alias="ItemID"
    )
    subcategory: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="Subcategory")
    size: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(45)), alias="Size")
    description: str = Field(sa_column=Column(mysql.VARCHAR(255), nullable=False), alias="Description")

    # Relationships
    item: "Items" = Relationship(back_populates="merchandise")
