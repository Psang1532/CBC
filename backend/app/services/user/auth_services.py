from fastapi import HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.repositories.user.student_repository import StudentRepository
from app.repositories.user.teacher_repository import TeacherRepository
from app.models.user.student import Student
from app.models.user.teacher import Teacher


class UserAuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student_repo = StudentRepository(session)
        self.teacher_repo = TeacherRepository(session)

    async def get_current_student(
        self, credentials: HTTPAuthorizationCredentials
    ) -> Student:
        """
        Extract and validate JWT token, then retrieve the Student from the database.
        
        Raises:
            HTTPException: If token is invalid or student not found
        """
        token = credentials.credentials

        # Decode the JWT token
        payload = decode_token(token)
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role != "student":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Retrieve student from database
        student = await self.student_repo.get_by_username(username)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Student not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return student

    async def get_current_teacher(
        self, credentials: HTTPAuthorizationCredentials
    ) -> Teacher:
        """
        Extract and validate JWT token, then retrieve the Teacher from the database.
        
        Raises:
            HTTPException: If token is invalid or teacher not found
        """
        token = credentials.credentials

        # Decode the JWT token
        payload = decode_token(token)
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Retrieve teacher from database
        teacher = await self.teacher_repo.get_by_username(username)

        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Teacher not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return teacher
