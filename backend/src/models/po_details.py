from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.mysql as mysql
from src.models import Supplies, PurchaseOrders

class PurchaseOrderDetails(SQLModel, table=True):
    __tablename__ = "orderdetails"
    
    order_details_id: int = Field(
        primary_key=True, 
        index=True, 
        sa_column=Column(mysql.INTEGER, nullable=False),
        alias="OrderDetailsID"
    )
    order_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        index=True,
        foreign_key="purchaseorders.OrderID",
        alias="OrderID"
    )
    supply_id: int = Field(
        sa_column=Column(mysql.INTEGER, nullable=False),
        index=True,
        foreign_key="supplies.SupplyID",
        alias="SupplyID"
    )
    quantity: int = Field(sa_column=Column(mysql.INTEGER, nullable=False, check="quantity > 0"), alias="Quantity")
    unit_price: float = Field(sa_column=Column(mysql.DECIMAL(10,2), nullable=False, check="unit_price > 0"), alias="UnitPrice")

    @property
    def subtotal(self): 
        return self.quantity * self.unit_price

    # Relationships
    purchase_order: "PurchaseOrders" = Relationship(back_populates="order_details")
    supply: "Supplies" = Relationship(back_populates="order_details")

