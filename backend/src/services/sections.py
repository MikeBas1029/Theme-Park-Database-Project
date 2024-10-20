from sqlmodel import select 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.models.sections import Section
from src.schemas.sections import SectionCreateModel, SectionUpdateModel

class SectionService:
    async def get_all_sections(self, session: AsyncSession):
        query = select(Section).order_by(Section.name)

        result = await session.exec(query)

        return result.all()
    
    async def get_section_by_id(self, section_id: str, session: AsyncSession):
        query = select(Section).where(Section.section_id == section_id)

        result = await session.exec(query)

        section = result.first()

        return section if section is not None else None 
    
    async def section_exists(self, section_id: str, session: AsyncSession):
        query = select(Section).where(Section.section_id == section_id)

        result = await session.exec(query)

        section = result.first()

        return bool(section)
    
    async def create_section(
            self,
            section_data: SectionCreateModel,
            session: AsyncSession
    ):
        section_data_dict = section_data.model_dump()

        new_section = Section(**section_data_dict)

        # First check if section exists already
        existing_section = await self.section_exists(new_section.section_id, session)

        if existing_section:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Section with section_id {new_section.section_id} already exists.")
        else:
            session.add(new_section)

            await session.commit()

            return new_section
    

    async def update_section(
            self, 
            section_id: str,
            update_data: SectionUpdateModel,
            session: AsyncSession
    ):
        section_to_update = await self.get_section_by_id(section_id, session)


        if section_to_update is not None:
            section_update_dict = update_data.model_dump()

            for k, v in section_update_dict.items():
                setattr(section_to_update, k, v)

            await session.commit()

            return section_to_update
        else:
            return None  
        
    async def delete_section(self, section_id: str, session: AsyncSession):
        section_to_delete = await self.get_section_by_id(section_id, session)

        if section_to_delete is not None:
            await session.delete(section_to_delete)
            await session.commit()

            return {}
        else:
            return None