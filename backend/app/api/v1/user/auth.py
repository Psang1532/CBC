# app/api/v1/routers/user/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from app.dependencies import get_async_db 
from app.core.security import create_access_token, create_refresh_token, decode_token, get_password_hash, verify_password
from app.models.user.student import Student
from app.models.user.teacher import Teacher
from app.repositories.user.student_repository import StudentRepository
from app.repositories.user.teacher_repository import TeacherRepository
from app.schemas.user.auth import Token, RefreshTokenRequest
from app.schemas.user.student import StudentCreate
from app.schemas.user.teacher import TeacherCreate

router = APIRouter()


@router.post("/register/student", response_model=Token)
async def register_student(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_async_db),
):
    repo = StudentRepository(db)

    # Check if username already exists (across both tables)
    username = student_in.full_name.strip()
    if await repo.get_by_username(username):
        raise HTTPException(
            status_code=400,
            detail="Username (full name) already registered"
        )
    if await repo.get_by_student_id(student_in.student_id):
        raise HTTPException(
            status_code=400,
            detail="Student ID already registered"
        )

    # Username = full_name (no case normalization)
    username = student_in.full_name.strip()

    student = Student(
        username=username,
        full_name=student_in.full_name,
        student_id=student_in.student_id,
        institution_name=student_in.institution_name,
        grade_level=student_in.grade_level,
        email=student_in.email,
        password_hash=get_password_hash(student_in.student_id),  # initial password = student_id
    )

    await repo.create(student)

    access_token = create_access_token(student.username, role="student")
    refresh_token = create_refresh_token(student.username, role="student")

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/register/teacher", response_model=Token)
async def register_teacher(
    teacher_in: TeacherCreate,
    db: AsyncSession = Depends(get_async_db),
):
    repo = TeacherRepository(db)

    username = teacher_in.full_name.strip()
    if await repo.get_by_username(username):
        raise HTTPException(
            status_code=400,
            detail="Username (full name) already registered"
        )
    if await repo.get_by_tsc_number(teacher_in.tsc_number):
        raise HTTPException(
            status_code=400,
            detail="TSC number already registered"
        )

    username = teacher_in.full_name.strip()

    teacher = Teacher(
        username=username,
        full_name=teacher_in.full_name,
        tsc_number=teacher_in.tsc_number,
        institution_name=teacher_in.institution_name,
        grade_levels_taught=teacher_in.grade_levels_taught,
        email=teacher_in.email,
        password_hash=get_password_hash(teacher_in.tsc_number),  # initial password = tsc_number
    )

    await repo.create(teacher)

    access_token = create_access_token(teacher.username, role="teacher")
    refresh_token = create_refresh_token(teacher.username, role="teacher")

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    # Try student first
    student_repo = StudentRepository(db)
    student = await student_repo.get_by_username(form_data.username)

    if student and verify_password(form_data.password, student.password_hash):
        access_token = create_access_token(student.username, role="student")
        refresh_token = create_refresh_token(student.username, role="student")
        return Token(access_token=access_token, refresh_token=refresh_token)

    # Then teacher
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_username(form_data.username)

    if teacher and verify_password(form_data.password, teacher.password_hash):
        access_token = create_access_token(teacher.username, role="teacher")
        refresh_token = create_refresh_token(teacher.username, role="teacher")
        return Token(access_token=access_token, refresh_token=refresh_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(payload: RefreshTokenRequest):
    """
    Exchange a refresh token for a new access token.
    Validates role claim from the refresh token.
    """
    token_data = decode_token(payload.refresh_token)
    username = token_data.get("sub")
    role = token_data.get("role")

    if not username or role not in {"student", "teacher"}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(username, role=role)
    return Token(
        access_token=access_token,
        refresh_token=payload.refresh_token,
        token_type="bearer",
    )