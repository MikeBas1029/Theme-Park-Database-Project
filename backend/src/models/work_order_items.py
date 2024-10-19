import sqlalchemy.dialects.mysql as mysql
from typing import List, TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Column, ForeignKey, Relationship

if TYPE_CHECKING:
    from src.models.purchase_order_items import PurchaseOrderItems 
    from src.models.work_orders import WorkOrders

class WorkOrderItems(SQLModel, table=True):
    __tablename__ = "workorderitems"

    id: int = Field(
        default=None,
        sa_column=Column(
            mysql.INTEGER,
            autoincrement=True,
            primary_key=True,
            nullable=False,
            comment="Unique identifier for items needed to be purchased for Work Orders."
        ),
        alias="WorkOrderItems"
    )

    woid: int = Field(
        default=None, 
        sa_column=Column(
            mysql.INTEGER,
            ForeignKey("workorder.woid"),
            nullable=False,
            comment="Foreign key to the Work Orders table",
        ),
        alias="WorkOrder"
    )

    po_item_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            mysql.INTEGER,
            ForeignKey("purchaseorderitems.id"),
            nullable=False,
            comment="Foreign key to the Purchase Order table.",
        ),
        alias="PurchaseOrder"
    )

    # Relationships
    work_order: "WorkOrders" = Relationship(back_populates="wo_items")
    purchase_order_item: Optional["PurchaseOrderItems"] = Relationship(back_populates="work_order_items")

