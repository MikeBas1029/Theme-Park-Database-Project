import string 
import secrets
import sqlalchemy.dialects.mysql as mysql
from typing import List, TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Column, ForeignKey, Relationship

if TYPE_CHECKING:
    from src.models.purchase_order_items import PurchaseOrderItems 
    from src.models.work_orders import WorkOrders

class WorkOrderItems(SQLModel, table=True):
    __tablename__ = "workorderitems"

    @staticmethod
    def generate_random_id(length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    

    id: str = Field(
        default_factory=lambda: WorkOrderItems.generate_random_id(),
        sa_column=Column(
            mysql.VARCHAR(12),
            primary_key=True,
            nullable=False,
            comment="Unique identifier for items needed to be purchased for Work Orders."
        ),
        alias="WorkOrderItems"
    )

    woid: str = Field(
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("workorder.woid"),
            nullable=False,
            comment="Foreign key to the Work Orders table",
        ),
        alias="WorkOrder"
    )

    po_item_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            mysql.VARCHAR(12),
            ForeignKey("purchaseorderitems.id"),
            nullable=False,
            comment="Foreign key to the Purchase Order table.",
        ),
        alias="PurchaseOrder"
    )

    # Relationships
    work_order: "WorkOrders" = Relationship(back_populates="wo_items")
    purchase_order_item: Optional["PurchaseOrderItems"] = Relationship(back_populates="work_order_items")

