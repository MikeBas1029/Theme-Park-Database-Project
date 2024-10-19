from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Index, ForeignKey
import sqlalchemy.dialects.mysql as mysql

if TYPE_CHECKING:
    from src.models.vendors import Vendors
    from src.models.beverage_items import BeverageItems
    from src.models.food_items import FoodItems
    from src.models.merchandise import Merchandise
    from src.models.rentals import Rentals
    from src.models.sales_order_details import SalesOrderDetail


class Items(SQLModel, table=True):
    __tablename__ = "items"
    
    # SKU (Stock Keeping Unit) serves as the unique identifier for each item.
    # This is the primary key for the table and is automatically incremented.
    sku: int = Field(
        default=None, 
        sa_column=Column(mysql.INTEGER, nullable=False, primary_key=True, autoincrement=True, comment="Unique identifier for each item (primary key)"),
        alias="SKU"
    )
    
    # Name of the item. This will store a string of up to 25 characters, and cannot be NULL.
    name: str = Field(sa_column=Column(mysql.VARCHAR(25), nullable=False, comment="Name of the item (up to 25 characters)"), alias="Name")
    
    # Category defines the type of item, either Merchandise, Concession, or Entertainment.
    # It uses an ENUM type to restrict values to the allowed categories.
    category: str = Field(
        sa_column=Column(mysql.ENUM("Merchandise", "Concession", "Entertainment"), nullable=False, comment="Category of the item (Merchandise, Concession, Entertainment)"),
        alias="Category"
    )
    
    # Price of the item in the database. This field cannot be NULL.
    # It stores the sale price of the item.
    price: float = Field(sa_column=Column(mysql.FLOAT, nullable=False, comment="Sale price of the item"), alias="Price")
    
    # Cost of the item to the business. This is used to calculate profit margins.
    # This field cannot be NULL.
    cost: float = Field(sa_column=Column(mysql.FLOAT, nullable=False, comment="Cost of the item to the business"), alias="Cost")
    
    # Status of the item. Indicates if the item is Active, Discontinued, or on Backorder.
    # Uses an ENUM type for restricted values.
    status: str = Field(
        sa_column=Column(mysql.ENUM("Active", "Discontinued", "Backorder"), nullable=False, comment="Status of the item (Active, Discontinued, or Backorder)"),
        alias="Status"
    )
    
    # Foreign key linking the item to a vendor. Each item must be supplied by a specific vendor.
    # The vendor_id is a reference to the VendorID column in the "vendors" table.
    vendor_id: int = Field(
        sa_column=Column(mysql.INTEGER, ForeignKey("vendors.vendor_id"), nullable=False, comment="Foreign key linking to the VendorID from the vendors table"),
        alias="VendorID"
    )

    # Relationships

    # Establishes a relationship between the Items model and the Vendors model.
    # The "vendor" field is populated with data from the "Vendors" table based on the vendor_id.
    vendor: "Vendors" = Relationship(back_populates="items")
    
    # Relationship to BeverageItems model: If this item belongs to the beverage category,
    # this relationship will link to the associated BeverageItems records.
    beverage_items: List["BeverageItems"] = Relationship(back_populates="item", cascade_delete=True)
    
    # Relationship to FoodItems model: If this item belongs to the food category,
    # this relationship will link to the associated FoodItems records.
    food_items: List["FoodItems"] = Relationship(back_populates="item", cascade_delete=True)
    
    # Relationship to Merchandise model: If this item belongs to the merchandise category,
    # this relationship will link to the associated Merchandise records.
    merchandise: List["Merchandise"] = Relationship(back_populates="item", cascade_delete=True)

    rentals: List["Rentals"] = Relationship(back_populates="item", cascade_delete=True)

    sales_order_details: List["SalesOrderDetail"] = Relationship(
        back_populates="item",
        cascade_delete=True,
    )

    # Table index: Adds an index on the "sku" column to speed up lookups based on SKU.
    # This ensures that queries filtering by SKU will be faster.
    __table_args__ = (Index("ix_items_sku", "sku"),)