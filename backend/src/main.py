import logging
from fastapi import FastAPI
from sqlmodel import SQLModel
from src.db.database import init_db
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import *
from src.routes import *
from src.errors import register_all_errors
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    await init_db()
    logger.info("Database intialized..")
    yield
    logger.info("Shutting down..")

version = "v1"
version_prefix = f"/api/{version}"

app = FastAPI(
    title="Theme Park Management",
    description="A REST API for a theme park company",
    version=version,
    lifespan=lifespan
)

register_all_errors(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(beverage_router, prefix=f"{version_prefix}/beverage", tags=["beverage"])
app.include_router(customer_router, prefix=f"{version_prefix}/customers", tags=["customers"])
app.include_router(cust_auth_router, prefix=f"{version_prefix}/cust-auth", tags=["customer auth"])
app.include_router(cust_notification_router, prefix=f"{version_prefix}/cust-notifs", tags=["customer notification"])
app.include_router(department_router, prefix=f"{version_prefix}/departments", tags=["departments"])
app.include_router(department_manager_router, prefix=f"{version_prefix}/department-managers", tags=["department managers"])
app.include_router(employee_router, prefix=f"{version_prefix}/employees", tags=["employees"])
app.include_router(emp_auth_router, prefix=f"{version_prefix}/emp-auth", tags=["emp_auth"])
app.include_router(employee_payment_router, prefix=f"{version_prefix}/employee-payments", tags=["employee payments"])
app.include_router(emp_notification_router, prefix=f"{version_prefix}/emp-notifs", tags=["employee notification"])
app.include_router(entertainment_router, prefix=f"{version_prefix}/entertainment", tags=["entertainment"])
app.include_router(food_item_router, prefix=f"{version_prefix}/food-items", tags=["food_items"])
app.include_router(guest_services_router, prefix=f"{version_prefix}/guest-services", tags=["guest_services"])
app.include_router(item_router, prefix=f"{version_prefix}/items", tags=["items"])
app.include_router(invoice_router, prefix=f"{version_prefix}/invoices", tags=["invoices"])
app.include_router(merchandise_router, prefix=f"{version_prefix}/merchandise", tags=["merchandise"])
app.include_router(park_facilities_router, prefix=f"{version_prefix}/park-factilities", tags=["park_factilities"])
app.include_router(payment_method_router, prefix=f"{version_prefix}/payment-methods", tags=["payment_methods"])
app.include_router(purchase_order_router, prefix=f"{version_prefix}/purchase-orders", tags=["purchase_orders"])
app.include_router(purchase_order_item_router, prefix=f"{version_prefix}/purchase-order-items", tags=["purchase_order_items"])
app.include_router(po_detail_router, prefix=f"{version_prefix}/purchase-order-details", tags=["purchase_order_details"])
app.include_router(rental_router, prefix=f"{version_prefix}/rentals", tags=["rentals"])
app.include_router(restaurant_router, prefix=f"{version_prefix}/restaurants", tags=["restaurants"])
app.include_router(ride_type_router, prefix=f"{version_prefix}/ride-type", tags=["ride_type"])
app.include_router(ride_usage_router, prefix=f"{version_prefix}/ride-usage", tags=["ride_usage"])
app.include_router(ride_router, prefix=f"{version_prefix}/rides", tags=["rides"])
app.include_router(sales_order_router, prefix=f"{version_prefix}/sales-orders", tags=["sales_order"])
app.include_router(sales_order_detail_router, prefix=f"{version_prefix}/sales-order-details", tags=["sales order detail"])
app.include_router(section_router, prefix=f"{version_prefix}/sections", tags=["section"])
app.include_router(shop_router, prefix=f"{version_prefix}/shops", tags=["shops"])
app.include_router(supplies_router, prefix=f"{version_prefix}/supplies", tags=["supplies"])
app.include_router(ticket_router, prefix=f"{version_prefix}/tickets", tags=["tickets"])
app.include_router(ticket_type_router, prefix=f"{version_prefix}/ticket-type", tags=["ticket types"])
app.include_router(timesheet_router, prefix=f"{version_prefix}/timesheets", tags=["timesheets"])
app.include_router(vendor_router, prefix=f"{version_prefix}/vendors", tags=["vendors"])
app.include_router(vendor_payment_router, prefix=f"{version_prefix}/vendor-payments", tags=["vendor payments"])
app.include_router(visit_router, prefix=f"{version_prefix}/visits", tags=["visits"])
app.include_router(visit_ticket_router, prefix=f"{version_prefix}/visit-ticket", tags=["visit ticket"])
app.include_router(work_order_router, prefix=f"{version_prefix}/work-orders", tags=["work orders"])
app.include_router(work_order_item_router, prefix=f"{version_prefix}/work-order-items", tags=["work order items"])
app.include_router(reports_router, prefix=f"{version_prefix}/reports", tags=["reports"])
