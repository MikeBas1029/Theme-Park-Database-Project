from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.employees import EmployeeService
from src.schemas.employees import Employee, EmployeeCreateModel, EmployeeUpdateModel

employee_router = APIRouter()
employee_service = EmployeeService()