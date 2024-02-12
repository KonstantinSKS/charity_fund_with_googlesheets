from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        query = select(CharityProject.name,
                       CharityProject.description,
                       (func.julianday(CharityProject.close_date) -
                        func.julianday(CharityProject.create_date)).label('collection_time')).where(
            CharityProject.fully_invested.is_(True)).order_by('collection_time')
        closed_projects = await session.execute(query)
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
