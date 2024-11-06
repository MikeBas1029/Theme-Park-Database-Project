from typing import List 
from sqlmodel import select
from sqlalchemy import text
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.models.views import MonthlyWeeklyCustomerCounts, FrequentRides, BrokenRides
from src.schemas.reports import MonthlyWeeklyCustomerCount, FrequentRide, BrokenRide, InvoiceStatus, HoursWorked

reports_router = APIRouter()

@reports_router.get("/customer-count", response_model=List[MonthlyWeeklyCustomerCount])
async def get_monthly_weekly_customer_counts(session: AsyncSession = Depends(get_session)):
    query = text('''
        SELECT Month AS month, Week AS week, Num_Customers AS num_customers 
        FROM `theme-park-db`.monthly_weekly_customer_counts;
    ''')
    result = await session.execute(query)
    rows = result.fetchall()
    # Convert each row to a dictionary
    return [{"month": row.month, "week": row.week, "num_customers": row.num_customers} for row in rows]

@reports_router.get("/frequent-rides", response_model=List[FrequentRide])
async def get_frequent_ride_counts(session: AsyncSession = Depends(get_session)):
    query = text('''
        SELECT month, name, num_rides 
        FROM `theme-park-db`.frequent_rides;
    ''')
    result = await session.execute(query)
    rows = result.fetchall()
    # Convert each row to a dictionary
    return [{"month": row.month, "name": row.name, "num_rides": row.num_rides} for row in rows]

@reports_router.get("/broken-rides", response_model=List[BrokenRide])
async def get_broken_rides(session: AsyncSession = Depends(get_session)):
    query = text('''
        SELECT Maintenance_Month AS maintenance_month, Num_Rides_Maintained AS num_rides_maintained, avg_rides_needing_maint 
        FROM `theme-park-db`.broken_rides;
    ''')
    result = await session.execute(query)
    rows = result.fetchall()
    # Convert each row to a dictionary
    return [{"Maintenance_Month": row.maintenance_month, "Num_Rides_Maintained": row.num_rides_maintained, "avg_rides_needing_maint": row.avg_rides_needing_maint} for row in rows]

@reports_router.get("/invoice-status", response_model=List[InvoiceStatus])
async def get_invoice_statuses(session: AsyncSession = Depends(get_session)):
    query = text('''
        SELECT inv.invoice_id, vend.company_name, sup.name AS supply, inv.amount_due, inv.payment_status
        FROM `theme-park-db`.invoice AS inv
        LEFT JOIN `theme-park-db`.purchaseorders AS po
        ON inv.po_number = po.order_id
        LEFT JOIN `theme-park-db`.vendors AS vend
        ON po.vendor_id = vend.vendor_id
        LEFT JOIN `theme-park-db`.orderdetails as po_det
        ON po.order_id = po_det.order_id
        LEFT JOIN `theme-park-db`.supplies as sup
        ON sup.supply_id = po_det.supply_id;
    ''')
    result = await session.execute(query)
    rows = result.fetchall()

    return [{"invoice_id": row.invoice_id, "company_name": row.company_name, "supply": row.supply, "amount_due": row.amount_due, "payment_status": row.payment_status} for row in rows]

@reports_router.get("/hours-worked", response_model=List[HoursWorked])
async def get_hours_worked(session: AsyncSession = Depends(get_session)):
    query = text('''
    SELECT 
        e.first_name,
        e.last_name,
        e.job_function,
        d.name AS department,
        YEAR(t.shift_date) as year,
        MONTHNAME(t.shift_date) as month,
        DAY(t.shift_date) as day,
        CASE 
            WHEN t.punch_in_time IS NOT NULL AND t.punch_out_time IS NOT NULL THEN 
                TIMESTAMPDIFF(MINUTE, t.punch_in_time, t.punch_out_time) / 60.0 
                - CASE 
                    WHEN t.meal_break_start IS NOT NULL AND t.meal_break_end IS NOT NULL THEN 
                        TIMESTAMPDIFF(MINUTE, t.meal_break_start, t.meal_break_end) / 60.0 
                    ELSE 0 
                END
            ELSE 0
        END AS hours_worked
    FROM `theme-park-db`.timesheet AS t
    LEFT JOIN `theme-park-db`.employees AS e
        ON t.employee_id = e.employee_id
    LEFT JOIN `theme-park-db`.sections AS s
        ON t.section_id = s.section_id
    LEFT JOIN `theme-park-db`.departments AS d
        ON s.department_id = d.department_id;
    ''')
    result = await session.execute(query)
    rows = result.fetchall()

    return [
        {
            "first_name": row.first_name, 
            "last_name": row.last_name, 
            "job_function": row.job_function, 
            "department": row.department, 
            "year": row.year,
            "month": row.month,
            "day": row.day,
            "hours_worked": row.hours_worked
        } for row in rows
        ]
