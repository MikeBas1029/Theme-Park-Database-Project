from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import init_db, get_session
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel
import logging
from src.models import *

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

app = FastAPI(
    title="Theme Park Management",
    description="A REST API for a theme park company",
    version=version,
    lifespan=lifespan
)

@app.get("/db-check")
async def db_check(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SHOW TABLES"))
    tables = [row[0] for row in result]
    return {"tables": tables}

@app.get("/db-test")
async def db_test(session: AsyncSession = Depends(get_session)):
    try:
        # Test basic query
        result = await session.execute(text("SELECT 1"))
        basic_query = result.scalar()

        # Test database name
        result = await session.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()

        # Test create table permission
        await session.execute(text("CREATE TABLE IF NOT EXISTS test_table (id INT)"))
        await session.commit()

        # Test if table was created
        result = await session.execute(text("SHOW TABLES LIKE 'test_table'"))
        test_table_exists = result.scalar() is not None

        # Clean up
        await session.execute(text("DROP TABLE IF EXISTS test_table"))
        await session.commit()

        return {
            "connection": "successful",
            "basic_query": basic_query,
            "database_name": db_name,
            "can_create_table": test_table_exists
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/create-test-table")
async def create_test_table(session: AsyncSession = Depends(get_session)):
    try:
        # Create a persistent test table
        await session.execute(text("CREATE TABLE IF NOT EXISTS persistent_test_table (id INT PRIMARY KEY AUTO_INCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
        await session.commit()

        # Insert a row
        await session.execute(text("INSERT INTO persistent_test_table (id) VALUES (DEFAULT)"))
        await session.commit()

        # Fetch data
        result = await session.execute(text("SELECT * FROM persistent_test_table"))
        data = result.fetchall()

        # Convert data to a list of dictionaries for JSON serialization
        formatted_data = [dict(row._mapping) for row in data]

        return {"message": "Test table created and populated", "data": formatted_data}
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemy error in create_test_table: {str(e)}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in create_test_table: {str(e)}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")