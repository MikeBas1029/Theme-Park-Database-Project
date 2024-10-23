import string 
import secrets
import sqlalchemy.dialects.mysql as mysql
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, ForeignKey, Relationship

if TYPE_CHECKING:
    from src.models.work_order_items import WorkOrderItems 
    from src.models.purchase_orders import PurchaseOrders
    from src.models.items import Items

class PurchaseOrderItems(SQLModel, table=True):
    __tablename__ = "purchaseorderitems"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    id: str = Field(
        default_factory=lambda: PurchaseOrderItems.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12),
            primary_key=True,
            nullable=False,
            comment="Primary key for po items."
        ),
        alias="POItemID"
    )

    item_id: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("items.sku"),
            nullable=False,
            comment="Unique identifier for items needed to be purchased for Work Orders."
        ),
        alias="ItemID"
    )

    poid: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("purchaseorders.order_id"),
            nullable=False,
            comment="Foreign key to the Purchase Order table.",
        ),
        alias="POID"
    )

    quantity: int = Field(
        sa_column=Column(
            mysql.INTEGER,
            nullable=False,
            comment="Quantity of items to be purchased",
        ),
        alias="Quantity"
    )

    # Relationships
    purchase_order: "PurchaseOrders" = Relationship(back_populates="po_items")
    item: "Items" = Relationship(back_populates="po_item")
    work_order_items: List["WorkOrderItems"] = Relationship(back_populates="purchase_order_item")
