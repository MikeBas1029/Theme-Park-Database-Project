from typing import List 
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.services.invoices import InvoiceService
from src.schemas.invoices import Invoice, InvoiceCreateModel, InvoiceUpdateModel

invoice_router = APIRouter()
invoice_service = InvoiceService()


@invoice_router.get("/", response_model=List[Invoice])
async def get_all_invoices(session: AsyncSession = Depends(get_session)):
    invoices = await invoice_service.get_all_invoices(session)
    return invoices


@invoice_router.get("/{invoice_id}", response_model=Invoice) 
async def get_invoice(invoice_id: str, session: AsyncSession = Depends(get_session)):
    invoice = await invoice_service.get_invoice_by_id(invoice_id, session)
    
    if invoice:
        return invoice
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with invoice {invoice_id} not found.") 



@invoice_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Invoice,
)
async def create_a_invoice(
    invoice_data: InvoiceCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        return await invoice_service.create_invoice(invoice_data, session)
    except Exception as error:
        raise error



@invoice_router.patch("/{invoice_id}", response_model=Invoice)
async def update_invoice(
    invoice_id: str,
    update_data: InvoiceUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    updated_invoice = await invoice_service.update_invoice(invoice_id, update_data, session)

    if updated_invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with invoice {invoice_id} not found.") 
    else:
        return updated_invoice


@invoice_router.delete(
    "/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_invoice(invoice_id: str, session: AsyncSession = Depends(get_session)):
    invoice_to_delete = await invoice_service.delete_invoice(invoice_id, session)
    
    if invoice_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invoice with invoice {invoice_id} not found.") 
