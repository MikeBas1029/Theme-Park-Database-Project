import enum
from typing import Optional
from pydantic import BaseModel

class FoodType(str, enum.Enum):
    snack = "Snack"
    meal = "Meal"
    dessert = "Dessert"
    candy = "Candy"

class FoodItemsOutputModel(BaseModel):
    food_id: str
    item_id: str
    food_type: FoodType
    calories: int
    ingredients: str
    serving_size: str

class FoodItemsInputModel(BaseModel):
    item_id: str
    food_type: FoodType
    calories: int
    ingredients: Optional[str | None] = None
    serving_size: Optional[str | None] = None 