from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.enterprise.project import EnterpriseProject
from .base import BaseRepository


class ProjectRepository(BaseRepository[EnterpriseProject]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EnterpriseProject)

    async def get_by_student(self, student_id: str) -> List[EnterpriseProject]:
        stmt = select(EnterpriseProject).where(EnterpriseProject.student_id == student_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_student_and_grade(
        self, student_id: str, grade_level: int
    ) -> EnterpriseProject | None:
        stmt = (
            select(EnterpriseProject)
            .where(EnterpriseProject.student_id == student_id)
            .where(EnterpriseProject.grade_level == grade_level)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
