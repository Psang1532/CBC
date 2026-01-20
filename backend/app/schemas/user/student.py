from typing import Optional
from datetime import datetime
from pydantic import Field

from ..base import BaseSchema


class StudentCreate(BaseSchema):
    """Registration input for students."""

    full_name: str = Field(..., min_length=2, max_length=100, description="Full name — will also be used as username")
    student_id: str = Field(..., min_length=3, max_length=50, description="Admission/registration number — also initial password")
    institution_name: str = Field(..., max_length=200)
    grade_level: int = Field(..., ge=10, le=12)
    email: Optional[str] = Field(None, description="Optional contact email")


class StudentUpdate(BaseSchema):
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None)
    institution_name: Optional[str] = Field(None, max_length=200)
    grade_level: Optional[int] = Field(None, ge=10, le=12)


class StudentRead(BaseSchema):
    id: int               # = full_name
    full_name: str
    student_id: str
    institution_name: str
    grade_level: int
    email: Optional[str]
    created_at: datetime