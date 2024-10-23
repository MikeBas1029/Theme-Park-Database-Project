from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.items import Items

class Merchandise(SQLModel, table=True):
    __tablename__ = "merchandise"
    
    # merchandise_id is the primary key for the Merchandise table, uniquely identifying each merchandise item.
    merchandise_id: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True, comment="Unique ID for each merchandise item"),
        alias="MerchandiseID"
    )
    
    # item_id is a foreign key referencing the SKU of an item in the Items table.
    item_id: str = Field(
        sa_column=Column(mysql.VARCHAR(12), ForeignKey("items.sku"), nullable=False, comment="Foreign key referencing SKU in the Items table"),
        alias="ItemID"
    )
    
    # subcategory represents the subcategory of the merchandise (e.g., "T-shirts", "Hats", etc.).
    subcategory: str = Field(
        sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="Subcategory of the merchandise"), 
        alias="Subcategory"
    )
    
    # size represents the size of the merchandise (e.g., "Small", "Medium", "Large") and is optional.
    size: Optional[str] = Field(
        sa_column=Column(mysql.VARCHAR(45), comment="Size of the merchandise item"), 
        alias="Size"
    )
    
    # description gives a detailed description of the merchandise item.
    description: str = Field(
        sa_column=Column(mysql.VARCHAR(255), nullable=False, comment="Description of the merchandise item"), 
        alias="Description"
    )

    # Relationships
    # Each merchandise item is associated with an item, represented by the `Items` model.
    item: "Items" = Relationship(back_populates="merchandise")

    # Table index: Adds an index to improve query performance on merchandise_id.
    __table_args__ = (
        Index("idx_merchandise_id", "merchandise_id"),
    )