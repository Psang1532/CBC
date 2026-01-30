from datetime import datetime

from app.schemas.base import BaseSchema


class ProjectFileBase(BaseSchema):
    filename: str
    filepath: str


class ProjectFileCreate(ProjectFileBase):
    pass


class ProjectFileRead(ProjectFileBase):
    id: str
    project_id: str
    created_at: datetime
