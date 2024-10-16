from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel  import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config 

# Create an asynchronous engine to interact with db
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))

async def init_db() -> None:
    '''Create all tables in the database defined using SQLModel'''
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    '''Define a database session to be used in database operations.'''
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session