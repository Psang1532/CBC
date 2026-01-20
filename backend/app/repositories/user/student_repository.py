# app/repositories/user/student_repository.py
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user.student import Student


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, student: Student) -> Student:
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def get_by_username(self, username: str) -> Optional[Student]:
        stmt = select(Student).where(Student.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_student_id(self, student_id: str) -> Optional[Student]:
        stmt = select(Student).where(Student.student_id == student_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()