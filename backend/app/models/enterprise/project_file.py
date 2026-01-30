from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from ..base import Base


class EnterpriseProjectFile(Base):
    __tablename__ = "enterprise_project_files"

    project_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("enterprise_projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filepath: Mapped[str] = mapped_column(String(500), nullable=False)

    project: Mapped["EnterpriseProject"] = relationship(
        "EnterpriseProject",
        back_populates="files"
    )


if TYPE_CHECKING:
    from .project import EnterpriseProject
