from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.enterprise.project_file import ProjectFile
from .base import BaseRepository


class ProjectFileRepository(BaseRepository[ProjectFile]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectFile)

    async def get_by_project(self, project_id: str) -> List[ProjectFile]:
        stmt = select(ProjectFile).where(ProjectFile.project_id == project_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_by_project(self, project_id: str) -> None:
        stmt = select(ProjectFile).where(ProjectFile.project_id == project_id)
        result = await self.session.execute(stmt)
        files = result.scalars().all()
        for file in files:
            await self.session.delete(file)
