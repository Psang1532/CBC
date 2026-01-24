from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.enterprise.student import Student
from .base import BaseRepository


class StudentRepository(BaseRepository[Student]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Student)

    async def get_by_student_id(self, student_id: str) -> Student | None:
        stmt = select(Student).where(Student.student_id == student_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
