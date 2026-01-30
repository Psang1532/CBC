# app/dependencies.py
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.repositories.user.student_repository import StudentRepository
from app.repositories.user.teacher_repository import TeacherRepository
from app.services.user.auth_services import UserAuthService
from app.models.user.student import Student
from app.models.user.teacher import Teacher

security = HTTPBearer()


async def get_async_db(db: AsyncSession = Depends(get_async_session)):
    yield db


def get_teacher_repo(db: AsyncSession = Depends(get_async_session)):
    return TeacherRepository(db)


def get_student_repo(db: AsyncSession = Depends(get_async_session)):
    return StudentRepository(db)


async def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session),
) -> Student:
    service = UserAuthService(db)
    return await service.get_current_student(credentials)


async def get_current_teacher(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session),
) -> Teacher:
    service = UserAuthService(db)
    return await service.get_current_teacher(credentials)