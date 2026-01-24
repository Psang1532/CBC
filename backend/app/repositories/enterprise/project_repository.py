from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.enterprise.project import Project
from .base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Project)

    async def get_by_student(self, student_id: str) -> List[Project]:
        stmt = select(Project).where(Project.student_id == student_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_student_and_grade(
        self, student_id: str, grade_level: int
    ) -> Project | None:
        stmt = (
            select(Project)
            .where(Project.student_id == student_id)
            .where(Project.grade_level == grade_level)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
