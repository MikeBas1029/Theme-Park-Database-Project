from typing import List
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Vendors, BeverageItems, FoodItems, Merchandise


class Items(SQLModel, table=True):
    __tablename__ = "items"
    
    sku: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="SKU"
    )
    name: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False), alias="Name")
    category: str = Field(
        sa_column=Column(mysql.ENUM("Merchandise", "Concession", "Entertainment"), nullable=False),
        alias="Category"
    )
    price: float = Field(sa_column=Column(mysql.FLOAT, nullable=False), alias="Price")
    cost: float = Field(sa_column=Column(mysql.FLOAT, nullable=False), alias="Cost")
    status: str = Field(
        sa_column=Column(mysql.ENUM("Active", "Discontinued", "Backorder"), nullable=False),
        alias="Status"
    )
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="vendors.VendorID",
        alias="VendorID"
    )

    # Relationships
    vendor: "Vendors" = Relationship(back_populates="items")
    beverage_items: List["BeverageItems"] = Relationship(back_populates="item")
    food_items: List["FoodItems"] = Relationship(back_populates="item")
    merchandise: List["Merchandise"] = Relationship(back_populates="item")
