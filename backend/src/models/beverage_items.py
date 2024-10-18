from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey, Index
import sqlalchemy.dialects.mysql as mysql
from typing import Optional
from src.models.items import Items

class BeverageItems(SQLModel, table=True):
    __tablename__ = "beverageitems"
    
    # bev_id is the primary key for the BeverageItems table, uniquely identifying each beverage item.
    bev_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True, comment="Unique ID for each beverage item"),
        alias="BevID"
    )
    
    # sku is a foreign key referencing the SKU of an item in the Items table.
    sku: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("items.sku"), nullable=False, comment="Foreign key referencing SKU in the Items table"),
        alias="SKU"
    )
    
    # drink_size represents the size of the beverage (e.g., "Small", "Medium", "Large").
    drink_size: str = Field(
        sa_column=Column(mysql.VARCHAR(20), nullable=False, comment="Size of the beverage"), 
        alias="DrinkSize"
    )
    
    # beverage_item defines the type of beverage (e.g., SODA, JUICE, WATER, OTHER).
    beverage_item: str = Field(
        sa_column=Column(mysql.ENUM("SODA", "JUICE", "WATER", "OTHER"), nullable=False, comment="Type of beverage item"),
        alias="BeverageItem"
    )
    
    # calories represents the calorie content of the beverage item (optional).
    calories: Optional[int] = Field(
        sa_column=Column(mysql.INTEGER, comment="Calorie content of the beverage item"), 
        alias="Calories"
    )

    # Relationships
    # A beverage item is associated with an item, represented by the `Items` model.
    item: "Items" = Relationship(back_populates="beverage_items")

    # Table indexes: Adds indexes to improve query performance on bev_id and sku.
    __table_args__ = (
        Index("idx_bev_id", "bev_id"),
        Index("idx_sku", "sku"),
    )