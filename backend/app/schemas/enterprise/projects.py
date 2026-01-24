from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    grade_level: int = Field(..., ge=10, le=12)


class ProjectCreate(ProjectBase):
    is_draft: bool = True


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_draft: Optional[bool] = None


class ProjectRead(ProjectBase):
    id: int
    student_id: str
    is_draft: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
