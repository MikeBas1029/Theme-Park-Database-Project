import enum
import string 
import secrets
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import Enum as SAEnum

if TYPE_CHECKING:
    from src.models.items import Items

class FoodType(str, enum.Enum):
    snack = "Snack"
    meal = "Meal"
    dessert = "Dessert"
    candy = "Candy"


class FoodItems(SQLModel, table=True):
    __tablename__ = "fooditems"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    

    # FoodID is the primary key for the food items table.
    # It uniquely identifies each food item.
    food_id: str = Field(
        default_factory=lambda: FoodItems.generate_random_id(),
        sa_column=Column(mysql.VARCHAR(12), nullable=False, primary_key=True, comment="Unique identifier for each food item (primary key)"),
        alias="FoodID"
    )

    # ItemID is a foreign key referencing the Items table.
    # It links each food item to a specific item in the 'items' table.
    item_id: str = Field(
        sa_column=Column(mysql.VARCHAR(12), ForeignKey("items.sku"), nullable=False, comment="Foreign key linking to the ItemID in the items table"),
        alias="ItemID"
    )

    # FoodType indicates the category of the food item.
    # It can be either 'SNACK', 'MEAL', or 'DESSERT' as defined in the ENUM.
    food_type: FoodType = Field(
        sa_column=Column(
            SAEnum(FoodType, values_callable=lambda x: [e.value for e in x]), 
            nullable=False, 
            comment="Category of the food item (e.g., SNACK, MEAL, DESSERT)"
        ),
        alias="FoodType"
    )

    # Calories is an optional field indicating the number of calories in the food item.
    # If not provided, this will be NULL.
    calories: Optional[int] = Field(
        sa_column=Column(mysql.INTEGER, comment="Number of calories in the food item"),
        alias="Calories"
    )

    # Ingredients is an optional field that lists the ingredients of the food item.
    # This is stored as a string and can be NULL if no information is available.
    ingredients: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(45), comment="Ingredients used in the food item"),
        alias="Ingredients"
    )

    # ServingSize is an optional field that describes the serving size of the food item.
    # It is stored as a string and can be NULL if not specified.
    serving_size: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(25), comment="Serving size of the food item"),
        alias="ServingSize"
    )

    # Relationships
    # Establishes a relationship between the FoodItems model and the Items model.
    # The "item" field is populated with data from the "Items" table based on the item_id.
    item: "Items" = Relationship(back_populates="food_items")

    # Table index: Adds an index on the food_id field.
    # This index improves performance for queries filtering by food_id.
    __table_args__ = (
        Index("idx_food_id", "food_id"),
    )