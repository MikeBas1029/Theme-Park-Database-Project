import sqlalchemy.dialects.mysql as mysql
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, ForeignKey, Relationship

if TYPE_CHECKING:
    from src.models.work_order_items import WorkOrderItems 
    from src.models.purchase_orders import PurchaseOrders

class PurchaseOrderItems(SQLModel, table=True):
    __tablename__ = "purchaseorderitems"

    id: int = Field(
        default=None,
        sa_column=Column(
            mysql.INTEGER,
            autoincrement=True,
            primary_key=True,
            nullable=False,
            comment="Unique identifier for items needed to be purchased for Work Orders."
        ),
        alias="PurchaseOrderItems"
    )

    poid: str = Field(
        default=None,
        sa_column=Column(
            mysql.VARCHAR(10),
            ForeignKey("purchaseorders.order_id"),
            nullable=False,
            comment="Foreign key to the Purchase Order table.",
        ),
        alias="PurchaseOrder"
    )

    # Relationships
    purchase_order: "PurchaseOrders" = Relationship(back_populates="po_items")
    work_order_items: List["WorkOrderItems"] = Relationship(back_populates="purchase_order_item")

