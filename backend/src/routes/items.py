from typing import List 
from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.items import ItemService
from src.schemas.items import Item, ItemCreateModel, ItemUpdateModel

item_router = APIRouter()
item_service = ItemService()

@item_router.get("/", response_model=List[Item])
async def get_all_items(session: AsyncSession = Depends(get_session)):
    items = await item_service.get_all_items(session)
    return items


@item_router.get("/{item_sku}", response_model=Item) 
async def get_item(item_sku: str, session: AsyncSession = Depends(get_session)):
    item = await item_service.get_item_by_sku(item_sku, session)
    
    if item:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with sku {item_sku} not found.") 



@item_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Item,
)
async def create_a_item(
    item_data: ItemCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await item_service.create_item(item_data, session)
    except Exception as error:
        raise error



@item_router.patch("/{item_sku}", response_model=Item)
async def update_item(
    item_sku: str,
    update_data: ItemUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_item = await item_service.update_item(item_sku, update_data, session)

    if updated_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with sku {item_sku} not found.") 
    else:
        return updated_item


@item_router.delete(
    "/{item_sku}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_item(item_sku: str, session: AsyncSession = Depends(get_session)):
    item_to_delete = await item_service.delete_item(item_sku, session)
    
    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with sku {item_sku} not found.") 