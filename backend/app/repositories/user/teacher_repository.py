# app/repositories/user/teacher_repository.py
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user.teacher import Teacher


class TeacherRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, teacher: Teacher) -> Teacher:
        self.session.add(teacher)
        await self.session.commit()
        await self.session.refresh(teacher)
        return teacher

    async def get_by_username(self, username: str) -> Optional[Teacher]:
        stmt = select(Teacher).where(Teacher.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_tsc_number(self, tsc_number: str) -> Optional[Teacher]:
        stmt = select(Teacher).where(Teacher.tsc_number == tsc_number)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()