from typing import List 
from fastapi import APIRouter, Depends, status 
from fastapi.exceptions import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.beverage_items import BeverageService
from src.schemas.beverage_items import Beverage, BeverageCreateModel, BeverageUpdateModel
from src.security import AccessTokenBearer

beverage_router = APIRouter()
beverage_service = BeverageService()
access_token_bearer = AccessTokenBearer()


@beverage_router.get("/", response_model=List[Beverage], dependencies=[Depends(AccessTokenBearer())])
async def get_all_beverages(
    session: AsyncSession = Depends(get_session)
    # _ : dict =Depends(access_token_bearer)
):
    # print(user_details)
    beverages = await beverage_service.get_all_beverages(session)
    return beverages


@beverage_router.get("/{bev_id}", response_model=Beverage) 
async def get_beverage(
    bev_id: str, 
    session: AsyncSession = Depends(get_session)
    # user_details=Depends(access_token_bearer)    
):
    beverage = await beverage_service.get_beverage_by_id(bev_id, session)
    
    if beverage:
        return beverage
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Beverage with id {bev_id} not found.") 



@beverage_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Beverage,
)
async def create_a_beverage(
    bev_data: BeverageCreateModel,
    session: AsyncSession = Depends(get_session)
    # user_details=Depends(access_token_bearer)

) -> dict:
    try:
        return await beverage_service.create_beverage(bev_data, session)
    except Exception as error:
        raise error



@beverage_router.patch("/{bev_id}", response_model=Beverage)
async def update_beverage(
    bev_id: str,
    update_data: BeverageUpdateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer)
) -> dict:
    updated_beverage = await beverage_service.update_bev(bev_id, update_data, session)

    if updated_beverage is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Beverage with id {bev_id} not found.") 
    else:
        return updated_beverage


@beverage_router.delete(
    "/{bev_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_beverage(
    bev_id: str, 
    session: AsyncSession = Depends(get_session), 
    user_details=Depends(access_token_bearer)
):
    beverage_to_delete = await beverage_service.delete_bev(bev_id, session)
    
    if beverage_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Beverage with id {bev_id} not found.") 
