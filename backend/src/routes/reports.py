from typing import List 
from sqlmodel import select
from sqlalchemy import text
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.models.views import MonthlyWeeklyCustomerCounts, FrequentRides, BrokenRides
from src.schemas.reports import MonthlyWeeklyCustomerCount, FrequentRide, BrokenRide, InvoiceStatus, HoursWorked, RideCount

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

@reports_router.get("/ride-counts", response_model=List[RideCount])
async def get_ride_counts(session: AsyncSession = Depends(get_session)):
    """
    Retrieve aggregated ride usage counts, grouped by year, month, week, and day.

    This endpoint returns a list of dictionaries containing ride usage statistics for each ride,
    organized by the ride's name, type, and various time dimensions (year, month, week, day).
    Aggregated counts are provided to capture the number of distinct usage occurrences at each time level.
    
    Args:
        session (AsyncSession): The asynchronous database session dependency injected into the function.
    
    Returns:
        List[RideCount]: A list of dictionaries, each representing usage statistics for a ride.
        Each dictionary includes:
            - ride_name (str): The name of the ride.
            - ride_type (str): The type of the ride (e.g., roller coaster, carousel).
            - year (int): The year of the usage event.
            - yearly_count (int): The count of unique years in which the ride was used.
            - month (str): The name of the month of the usage event.
            - monthly_count (int): The count of unique year-month combinations for monthly usage.
            - week (int): The week number within the year.
            - weekly_count (int): The count of unique year-week combinations for weekly usage.
            - day (int): The day of the usage event.
            - daily_count (int): The count of unique usage dates.
    """
    query = text('''
    SELECT 
        r.name AS ride_name,
        rt.ride_type,
        YEAR(ru.usage_date) as year,
        COUNT(DISTINCT YEAR(ru.usage_date)) AS yearly_count,
        MONTHNAME(ru.usage_date) as month,
        COUNT(DISTINCT CONCAT(YEAR(ru.usage_date), '-', MONTH(ru.usage_date))) AS monthly_count,
        WEEK(ru.usage_date) as week,
        COUNT(DISTINCT CONCAT(YEAR(ru.usage_date), '-', WEEK(ru.usage_date))) AS weekly_count,
        DAY(ru.usage_date) as day,
        COUNT(DISTINCT ru.usage_date) AS daily_count
    FROM `theme-park-db`.rides AS r
    LEFT JOIN `theme-park-db`.ride_usage AS ru
    ON r.ride_id = ru.ride_id
    LEFT JOIN `theme-park-db`.ride_type AS rt
    ON rt.ride_type_id = r.ride_type
    GROUP BY 
        r.name, 
        r.ride_type,
        YEAR(ru.usage_date),
        MONTHNAME(ru.usage_date),
        WEEK(ru.usage_date),
        DAY(ru.usage_date)
    ORDER BY 
        r.name, 
        r.ride_type;
    ''')
    result = await session.execute(query)
    rows = result.fetchall()
    # Convert each row to a dictionary
    return [
        {
            "ride_name": row.ride_name, 
            "ride_type": row.ride_type, 
            "year": row.year,
            "yearly_count": row.yearly_count,
            "month": row.month,
            "monthly_count": row.monthly_count,
            "week": row.week,
            "weekly_count": row.weekly_count,
            "day": row.day,
            "daily_count": row.daily_count
        } for row in rows
        ]

@reports_router.get("/broken-rides", response_model=List[BrokenRide])
async def get_broken_rides(session: AsyncSession = Depends(get_session)):
    """
    Retrieve a report of rides currently closed for maintenance or repair, 
    including the most recent work order details.

    This endpoint fetches a list of rides that are currently marked as 
    'CLOSED(M)' (Closed for Maintenance) or 'CLOSED(R)' (Closed due to Rainout) 
    from the `rides` table. 
    
    For each ride, it includes details from the latest work order, as well as 
    the employee assigned to the work order. The information provided includes:

    - Ride name
    - Last inspection date
    - Ride status
    - Assigned employee's full name
    - Maintenance type of the work order
    - Creation date of the work order
    - Status of the work order

    This report is helpful for tracking rides that are out of operation and 
    assessing current maintenance or repair activities.

    Parameters:
    - `session` (AsyncSession): Database session dependency.

    Returns:
    - `List[BrokenRide]`: A list of rides with the latest maintenance or 
    repair work order information.
    """

    query = text('''
    SELECT 
        r.name as ride_name,
        r.last_inspected,
        r.status as ride_status,
        CONCAT(e.first_name, ' ', e.last_name) as assigned_employee,
        wo.maintenance_type,
        wo.date_created,
        wo.status as wo_status
    FROM `theme-park-db`.rides as r
    LEFT JOIN `theme-park-db`.workorder as wo
    ON r.ride_id = wo.ride_id
    LEFT JOIN `theme-park-db`.employees as e 
    ON wo.assigned_worker_id = e.employee_id
    WHERE
        wo.date_created = (
        SELECT MAX(date_created)
        FROM `theme-park-db`.workorder
        WHERE ride_id = r.ride_id
        ) 
        AND wo.ride_id IS NOT NULL
        AND r.status in ('CLOSED(M)', 'CLOSED(R)');
    ''')
    result = await session.execute(query)
    rows = result.fetchall()
    # Convert each row to a dictionary
    return [
        {
            "ride_name": row.ride_name, 
            "last_inspected": row.last_inspected, 
            "ride_status": row.ride_status,
            "assigned_employee": row.assigned_employee,
            "maintenance_type": row.maintenance_type,
            "date_created": row.date_created,
            "wo_status": row.wo_status
        } for row in rows
        ]


@reports_router.get("/invoice-status", response_model=List[InvoiceStatus])
async def get_invoice_statuses(session: AsyncSession = Depends(get_session)):
    """
    Retrieve the status of invoices, including vendor information and related 
    supply details.

    This endpoint provides a report of all invoices in the system, showing key 
    details for tracking outstanding payments and associated vendors. 
    The information includes:

    - Invoice ID
    - Vendor's company name
    - Name of the supply item related to the invoice
    - Amount due for the invoice
    - Payment status of the invoice

    This report is helpful for monitoring financial transactions with vendors and 
    tracking the status of payments.

    Parameters:
    - `session` (AsyncSession): Database session dependency.

    Returns:
    - `List[InvoiceStatus]`: A list of invoices with vendor, supply, and payment 
    status information.
    """

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

    return [
        {
            "invoice_id": row.invoice_id, 
            "company_name": row.company_name, 
            "supply": row.supply, 
            "amount_due": row.amount_due, 
            "payment_status": row.payment_status
        } for row in rows
        ]

@reports_router.get("/hours-worked", response_model=List[HoursWorked])
async def get_hours_worked(session: AsyncSession = Depends(get_session)):
    """
    Retrieve a report of hours worked by hourly employees factoring in 
    meal breaks, where applicable.

    This endpoint generates a report on the total hours worked by each 
    employee, broken down by day. It calculates the hours worked by factoring 
    in punch-in and punch-out times and subtracting any meal break time if 
    applicable. The information includes:

    - Employee's first and last name
    - Job function of the employee
    - Department where the employee worked
    - Year, month, and day of the shift
    - Total hours worked (excluding meal breaks)

    This report is useful for tracking daily work hours by employees across 
    different departments and assessing labor distribution.

    Parameters:
    - `session` (AsyncSession): Database session dependency.

    Returns:
    - `List[HoursWorked]`: A list of daily work records with employee and 
    department details, and hours worked.
    """
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