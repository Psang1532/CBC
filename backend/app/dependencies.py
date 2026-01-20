# app/dependencies.py
from app.repositories.user.student_repository import StudentRepository
from app.repositories.user.teacher_repository import TeacherRepository
from fastapi import Depends
from app.db.session import get_async_session  # ← your session factory

async def get_async_db(db = Depends(get_async_session)):
    yield db

def get_teacher_repo(db=Depends(get_async_session)):
    return TeacherRepository(db)

def get_student_repo(db=Depends(get_async_session)):
    return StudentRepository(db)