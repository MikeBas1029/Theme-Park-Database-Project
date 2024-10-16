from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from datetime import datetime, date, time
from typing import Optional, List
from enum import Enum
from src.models import Items

class BeverageItems(SQLModel, table=True):
    __tablename__ = "beverageitems"
    
    bev_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="BevID"
    )
    sku: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="items.SKU",
        alias="SKU"
    )
    drink_size: str = Field(sa_column=Column(mysql.VARCHAR(20), nullable=False), alias="DrinkSize")
    beverage_item: str = Field(
        sa_column=Column(mysql.ENUM("SODA", "JUICE", "WATER", "OTHER"), nullable=False),
        alias="BeverageItem"
    )
    calories: Optional[int] = Field(sa_column=Column(mysql.INTEGER), alias="Calories")

    # Relationships
    item: "Items" = Relationship(back_populates="beverage_items")
