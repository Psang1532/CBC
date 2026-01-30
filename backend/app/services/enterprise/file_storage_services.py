import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, HTTPException, status

from app.core.storage import ENTERPRISE_PROJECTS_PATH


MAX_FILE_SIZE_MB = 25
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx"}


class EnterpriseFileStorageService:
    @staticmethod
    def _validate_file(file: UploadFile):
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {ext}",
            )

    @staticmethod
    def _validate_file_size(file: UploadFile):
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File exceeds 25MB limit",
            )

        return size

    @staticmethod
    def project_directory(
        student_id: str,
        grade_level: int,
        project_id: str,
    ) -> Path:
        return (
            ENTERPRISE_PROJECTS_PATH
            / student_id
            / f"grade_{grade_level}"
            / project_id
        )

    @classmethod
    def clear_project_files(
        cls,
        student_id: str,
        grade_level: int,
        project_id: str,
    ):
        path = cls.project_directory(student_id, grade_level, project_id)
        if path.exists():
            shutil.rmtree(path)

    @classmethod
    def save_files(
        cls,
        *,
        student_id: str,
        grade_level: int,
        project_id: str,
        files: list[UploadFile],
    ) -> list[dict]:
        base_dir = cls.project_directory(student_id, grade_level, project_id)
        base_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []

        for file in files:
            cls._validate_file(file)
            size = cls._validate_file_size(file)

            stored_name = f"{uuid4()}{Path(file.filename).suffix}"
            file_path = base_dir / stored_name

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            saved_files.append(
                {
                    "filename": stored_name,
                    "filepath": str(file_path),
                }
            )

        return saved_files
