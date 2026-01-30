from typing import List, TYPE_CHECKING
from sqlalchemy import String, Integer, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base
import enum


class ProjectStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    REJECTED = "REJECTED"


class EnterpriseProject(Base):
    __tablename__ = "enterprise_projects"

    student_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    grade_level: Mapped[int] = mapped_column(Integer, nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    designation: Mapped[str] = mapped_column(String(255), nullable=False)
    county_of_origin: Mapped[str] = mapped_column(String(255), nullable=False)
    idea_description: Mapped[str] = mapped_column(String(2000), nullable=False)

    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False, default=ProjectStatus.DRAFT
    )

    files: Mapped[List["EnterpriseProjectFile"]] = relationship(
        "EnterpriseProjectFile",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="joined",
    )


if TYPE_CHECKING:
    from .project_file import EnterpriseProjectFile

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "grade_level",
            name="uq_student_grade_project"
        ),
    )
