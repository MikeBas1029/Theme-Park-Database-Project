import logging
from fastapi import FastAPI
from sqlmodel import SQLModel
from src.db.database import init_db
from src.routes.customers import customer_router
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import *
from src.routes import items

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    logger.info("SQLModel subclasses..")
    for model in SQLModel.__subclasses__():
        logger.info(f" - {model.__name__}")
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
app.include_router(items.item_router, prefix="/items", tags=["Items"])