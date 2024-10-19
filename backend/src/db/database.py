from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel  import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import ssl
from src.config import Config 
from .triggers import birthday_discount_trigger, change_status_if_not_inspected

import logging 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

# SSL Certificate
ssl_context = ssl.create_default_context(cafile=Config.SSL_CERT)

# Create an asynchronous engine to interact with db
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, connect_args={"ssl": ssl_context}))

async def init_db() -> None:
    try:
        logging.info("Starting database initialization...")
        
        # Print all models that should be creating tables
        model_classes = SQLModel.__subclasses__()
        logging.info(f"Found {len(model_classes)} SQLModel subclasses:")
        for model in model_classes:
            logging.info(f"  - {model.__name__}")
        
        async with async_engine.begin() as conn:
            logging.info("Creating tables...")
            await conn.run_sync(SQLModel.metadata.create_all)

            # Create trigger to check last inspection on ride
            await conn.execute(birthday_discount_trigger)

            # Birthday discount trigger
            await conn.execute(change_status_if_not_inspected)
   
        logging.info("Checking created tables...")
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            logging.info(f"Tables in database: {', '.join(tables) if tables else 'No tables found'}")
        
        logging.info("Database initialization complete.")
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemy error during database initialization: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during database initialization: {str(e)}")
        raise

async def get_session() -> AsyncSession:
    '''Define a database session to be used in database operations.'''
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with Session() as session:
        yield session