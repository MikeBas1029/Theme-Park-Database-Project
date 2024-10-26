from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.invoices import Invoice
from src.schemas.invoices import InvoiceCreateModel, InvoiceUpdateModel

class InvoiceService:
    async def get_all_invoices(self, session: AsyncSession):
        query = select(Invoice).order_by(Invoice.due_date)

        result = await session.exec(query)

        return result.all()
    
    async def get_invoice_by_id(self, invoice_id: str, session: AsyncSession):
        query = select(Invoice).where(Invoice.invoice_id == invoice_id)

        result = await session.exec(query)

        invoice = result.first()

        return invoice if invoice is not None else None 
    
    async def invoice_exists(self, invoice_id: str, session: AsyncSession):
        query = select(Invoice).where(Invoice.invoice_id == invoice_id)

        result = await session.exec(query)

        invoice = result.first()

        return bool(invoice)
    
    async def create_invoice(
            self,
            invoice_data: InvoiceCreateModel,
            session: AsyncSession
    ):
        invoice_data_dict = invoice_data.model_dump()

        new_invoice = Invoice(**invoice_data_dict)

        # First check if invoice exists already
        existing_invoice = await self.invoice_exists(new_invoice.invoice_id, session)

        if existing_invoice:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Invoice with invoice_id {new_invoice.invoice_id} already exists.")
        else:
            session.add(new_invoice)

            await session.commit()

            return new_invoice
    

    async def update_invoice(
            self, 
            invoice_id: str,
            update_data: InvoiceUpdateModel,
            session: AsyncSession
    ):
        invoice_to_update = await self.get_invoice_by_id(invoice_id, session)


        if invoice_to_update is not None:
            invoice_update_dict = update_data.model_dump()

            for k, v in invoice_update_dict.items():
                setattr(invoice_to_update, k, v)

            await session.commit()

            return invoice_to_update
        else:
            return None  
        
    async def delete_invoice(self, invoice_id: str, session: AsyncSession):
        invoice_to_delete = await self.get_invoice_by_id(invoice_id, session)

        if invoice_to_delete is not None:
            await session.delete(invoice_to_delete)
            await session.commit()

            return {}
        else:
            return None