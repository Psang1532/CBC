from typing import List

from app.models.enterprise.project import EnterpriseProject, ProjectStatus
from app.models.enterprise.project_file import EnterpriseProjectFile as ProjectFile
from app.repositories.enterprise.project_repository import ProjectRepository
from app.repositories.enterprise.project_file_repository import ProjectFileRepository


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        project_file_repo: ProjectFileRepository,
    ):
        self.project_repo = project_repo
        self.project_file_repo = project_file_repo

    # ---------------------------------------------------------
    # Draft Creation
    # ---------------------------------------------------------

    async def create_or_replace_draft(
        self,
        *,
        student_id: str,
        grade_level: int,
        title: str,
        designation: str,
        county_of_origin: str,
        idea_description: str,
    ) -> EnterpriseProject:
        """
        Ensures a single draft exists per student per grade.
        If a draft already exists, it is replaced.
        """

        existing = await self.project_repo.get_by_student_and_grade(
            student_id=student_id,
            grade_level=grade_level,
        )

        if existing:
            if existing.status != ProjectStatus.DRAFT:
                raise ValueError(
                    "Cannot modify a project that is not in draft state."
                )

            existing.title = title
            existing.designation = designation
            existing.county_of_origin = county_of_origin
            existing.idea_description = idea_description
            return existing

        project = EnterpriseProject(
            student_id=student_id,
            grade_level=grade_level,
            title=title,
            designation=designation,
            county_of_origin=county_of_origin,
            idea_description=idea_description,
            status=ProjectStatus.DRAFT,
        )

        await self.project_repo.add(project)
        return project

    # ---------------------------------------------------------
    # File Handling (Metadata Only)
    # ---------------------------------------------------------

    async def attach_files_to_project(
        self,
        *,
        project: EnterpriseProject,
        files: List[dict],
    ) -> None:
        """
        Files are assumed to be already saved on disk.
        This method stores metadata only.
        """

        if project.status not in {ProjectStatus.DRAFT, ProjectStatus.REJECTED}:
            raise ValueError("Files can only be attached to draft or rejected projects.")

        for file in files:
            project_file = ProjectFile(
                project_id=project.id,
                filename=file["filename"],
                filepath=file["filepath"],
            )
            await self.project_file_repo.add(project_file)

    async def replace_project_files(
        self,
        *,
        project: EnterpriseProject,
        new_files: List[dict],
    ) -> None:
        """
        Used during resubmission.
        All previous files are deleted and replaced.
        """

        await self.project_file_repo.delete_by_project(project.id)
        await self.attach_files_to_project(project=project, files=new_files)

    # ---------------------------------------------------------
    # Submission
    # ---------------------------------------------------------

    async def submit_project(self, *, project: EnterpriseProject) -> EnterpriseProject:
        """
        Locks project from further student edits.
        """

        if project.status != ProjectStatus.DRAFT:
            raise ValueError("Only draft projects can be submitted.")

        project.status = ProjectStatus.SUBMITTED
        return project

    # ---------------------------------------------------------
    # Resubmission
    # ---------------------------------------------------------

    async def resubmit_project(self, *, project: EnterpriseProject) -> EnterpriseProject:
        """
        Allowed only after rejection.
        """

        if project.status != ProjectStatus.REJECTED:
            raise ValueError("Only rejected projects can be resubmitted.")

        project.status = ProjectStatus.SUBMITTED
        return project

    # ---------------------------------------------------------
    # Student Visibility
    # ---------------------------------------------------------

    async def list_student_projects(self, *, student_id: str) -> List[EnterpriseProject]:
        """
        Students can see drafts, submitted, rejected, graded projects.
        """

        return await self.project_repo.get_by_student(student_id)
