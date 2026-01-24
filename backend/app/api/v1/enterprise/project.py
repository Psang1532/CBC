from typing import List

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.dependencies import get_current_student

from app.schemas.enterprise import (
    ProjectCreateSchema,
    ProjectReadSchema,
)

from app.repositories.enterprise.project_repository import ProjectRepository
from app.repositories.enterprise.project_file_repository import ProjectFileRepository

from app.services.enterprise.project_services import ProjectService


router = APIRouter(
    prefix="/enterprise/projects",
    tags=["Social Enterprise Projects"],
)


# ---------------------------------------------------------------------
# Create or update a SINGLE draft per grade level
# ---------------------------------------------------------------------
@router.post(
    "/draft",
    response_model=ProjectReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_or_update_draft(
    payload: ProjectCreateSchema,
    db: AsyncSession = Depends(get_async_db),
    student=Depends(get_current_student),
):
    """
    Create or update a draft Social Enterprise project.

    Rules:
    - One project per student per grade level
    - Draft is overwritten if it already exists
    - Only students can access this endpoint
    """

    service = ProjectService(
        project_repo=ProjectRepository(db),
        file_repo=ProjectFileRepository(db),
    )

    project = await service.create_or_replace_draft(
        student_id=student.student_id,
        grade_level=payload.grade_level,
        title=payload.title,
        designation=payload.designation,
        county_of_origin=payload.county_of_origin,
        idea_description=payload.idea_description,
    )

    return project


# ---------------------------------------------------------------------
# Upload multiple files (draft or rejected only)
# ---------------------------------------------------------------------
@router.post("/draft/files", status_code=status.HTTP_200_OK)
async def upload_project_files(
    project_id: str,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_async_db),
    student=Depends(get_current_student),
):
    """
    Upload multiple files for a project.

    Constraints:
    - Allowed only if project status is DRAFT or REJECTED
    - Resubmission replaces all previous files
    - Max file size enforcement handled in service/storage layer
    """

    project_repo = ProjectRepository(db)
    project = await project_repo.get_by_id(project_id)

    if not project or project.student_id != student.student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if project.status not in ("draft", "rejected"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Files cannot be uploaded at this stage",
        )

    service = ProjectService(
        project_repo=project_repo,
        file_repo=ProjectFileRepository(db),
    )

    await service.replace_project_files(
        project=project,
        uploaded_files=files,
    )

    return {"detail": "Files uploaded successfully"}


# ---------------------------------------------------------------------
# Submit project (final submission)
# ---------------------------------------------------------------------
@router.post("/{project_id}/submit", status_code=status.HTTP_200_OK)
async def submit_project(
    project_id: str,
    db: AsyncSession = Depends(get_async_db),
    student=Depends(get_current_student),
):
    """
    Final submission of a project.

    Effects:
    - Locks the project from student edits
    - Changes status to SUBMITTED
    """

    repo = ProjectRepository(db)
    project = await repo.get_by_id(project_id)

    if not project or project.student_id != student.student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    service = ProjectService(
        project_repo=repo,
        file_repo=ProjectFileRepository(db),
    )

    await service.submit_project(project)

    return {"detail": "Project submitted successfully"}


# ---------------------------------------------------------------------
# Resubmit project after rejection
# ---------------------------------------------------------------------
@router.post("/{project_id}/resubmit", status_code=status.HTTP_200_OK)
async def resubmit_project(
    project_id: str,
    db: AsyncSession = Depends(get_async_db),
    student=Depends(get_current_student),
):
    """
    Resubmit a rejected project.

    Rules:
    - Allowed only if status == REJECTED
    - Existing files are replaced
    """

    repo = ProjectRepository(db)
    project = await repo.get_by_id(project_id)

    if not project or project.student_id != student.student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    service = ProjectService(
        project_repo=repo,
        file_repo=ProjectFileRepository(db),
    )

    await service.resubmit_project(project)

    return {"detail": "Project resubmitted successfully"}


# ---------------------------------------------------------------------
# List all projects for the logged-in student
# ---------------------------------------------------------------------
@router.get(
    "/my-projects",
    response_model=List[ProjectReadSchema],
    status_code=status.HTTP_200_OK,
)
async def list_my_projects(
    db: AsyncSession = Depends(get_async_db),
    student=Depends(get_current_student),
):
    """
    Retrieve all projects for the logged-in student.

    Includes:
    - Drafts
    - Submitted projects
    - Rejected projects
    """

    repo = ProjectRepository(db)
    return await repo.get_by_student(student.student_id)
