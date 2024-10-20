from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.items import ItemService
from src.schemas.items import Item, ItemCreateModel, ItemUpdateModel

item_router = APIRouter()
item_service = ItemService()

# Get all items
@item_router.get("/", response_model=List[Item])
async def get_all_items(session: AsyncSession = Depends(get_session)):
    items = await item_service.get_all_items(session)
    return items

# Get an item by SKU
@item_router.get("/{sku}", response_model=Item)
async def get_item(sku: int, session: AsyncSession = Depends(get_session)):
    item = await item_service.get_item_by_sku(sku, session)

    if item:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with SKU {sku} not found.")

# Create a new item
@item_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Item)
async def create_an_item(item_data: ItemCreateModel, session: AsyncSession = Depends(get_session)):
    try:
        return await item_service.create_item(item_data, session)
    except Exception as error:
        raise error

# Update an item by SKU
@item_router.patch("/{sku}", response_model=Item)
async def update_item(sku: int, update_data: ItemUpdateModel, session: AsyncSession = Depends(get_session)):
    updated_item = await item_service.update_item(sku, update_data, session)

    if updated_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with SKU {sku} not found.")
    else:
        return updated_item

# Delete an item by SKU
@item_router.delete("/{sku}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(sku: int, session: AsyncSession = Depends(get_session)):
    item_to_delete = await item_service.delete_item(sku, session)

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with SKU {sku} not found.")
