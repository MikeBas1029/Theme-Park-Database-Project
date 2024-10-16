from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

version = "v1"
app = FastAPI(
    title="Theme Park Management",
    description="A REST API for a theme park company",
    version=version,
    lifespan=lifespan
)