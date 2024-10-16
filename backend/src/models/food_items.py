from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Items

class FoodItems(SQLModel, table=True):
    __tablename__ = "fooditems"
    
    food_id: int = Field(
        default=None, 
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False, autoincrement=True),
        alias="FoodID"
    )
    item_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        foreign_key="items.SKU",
        alias="ItemID"
    )
    food_type: str = Field(
        sa_column=Column(mysql.ENUM("SNACK", "MEAL", "DESSERT"), nullable=False),
        alias="FoodType"
    )
    calories: Optional[int] = Field(sa_column=Column(mysql.INTEGER), alias="Calories")
    ingredients: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(45)), alias="Ingredients")
    serving_size: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(25)), alias="ServingSize")

    # Relationships
    item: "Items" = Relationship(back_populates="food_items")
