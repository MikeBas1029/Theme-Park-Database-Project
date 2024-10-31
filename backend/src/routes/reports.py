from typing import List 
from sqlmodel import select
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.models.views import MonthlyWeeklyCustomerCounts, FrequentRides
from src.schemas.reports import MonthlyWeeklyCustomerCount, FrequentRide

reports_router = APIRouter()


@reports_router.get("/customer-count", response_model=List[MonthlyWeeklyCustomerCount])
async def get_monthly_weekly_customer_counts(session: AsyncSession = Depends(get_session)):
    query = select(MonthlyWeeklyCustomerCounts)
    result = await session.exec(query)

    return result.all()

@reports_router.get("/frequent-rides", response_model=List[FrequentRide])
async def get_frequent_ride_counts(session: AsyncSession = Depends(get_session)):
    query = select(FrequentRides)
    results = await session.exec(query)
    return results.all()
