from datetime import datetime
from typing import Optional

from pydantic import Field

from app.models.enterprise.project import ProjectStatus
from app.schemas.base import BaseSchema


class ProjectBase(BaseSchema):
    title: str
    designation: str
    county_of_origin: str
    idea_description: str
    grade_level: int = Field(..., ge=10, le=12)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseSchema):
    title: Optional[str] = None
    designation: Optional[str] = None
    county_of_origin: Optional[str] = None
    idea_description: Optional[str] = None


class ProjectRead(ProjectBase):
    id: str
    student_id: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
