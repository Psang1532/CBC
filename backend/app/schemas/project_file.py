from pydantic import BaseModel
from datetime import datetime


class ProjectFileBase(BaseModel):
    filename: str


class ProjectFileCreate(ProjectFileBase):
    pass


class ProjectFileRead(ProjectFileBase):
    id: int
    project_id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
