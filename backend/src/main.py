import logging
from fastapi import FastAPI
from sqlmodel import SQLModel
from src.db.database import init_db
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import *
from src.routes import *


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

app.include_router(customer_router, prefix=f"{version_prefix}/customers", tags=["customers"])
app.include_router(employee_router, prefix=f"{version_prefix}/employees", tags=["employees"])
app.include_router(department_router, prefix=f"{version_prefix}/departments", tags=["departments"])
app.include_router(visit_router, prefix=f"{version_prefix}/visits", tags=["visits"])
app.include_router(section_router, prefix=f"{version_prefix}/section", tags=["section"])
app.include_router(ride_type_router, prefix=f"{version_prefix}/ridetype", tags=["ride_type"])
app.include_router(ride_router, prefix=f"{version_prefix}/rides", tags=["rides"])
app.include_router(ride_usage_router, prefix=f"{version_prefix}/rideusage", tags=["ride_usage"])
app.include_router(beverage_router, prefix=f"{version_prefix}/beverage", tags=["beverage"])
app.include_router(payment_method_router, prefix=f"{version_prefix}/paymentmethods", tags=["payment_methods"])
app.include_router(employee_payment_router, prefix=f"{version_prefix}/employeepayments", tags=["employee_payments"])