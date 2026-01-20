from typing import List, Optional

from pydantic import Field
from datetime import datetime

from ..base import BaseSchema


class TeacherCreate(BaseSchema):
    """Registration input for teachers."""

    full_name: str = Field(..., min_length=2, max_length=100, description="Full name — will also be used as username")
    tsc_number: str = Field(..., min_length=5, max_length=50, description="TSC number — also initial password")
    institution_name: str = Field(..., max_length=200)
    grade_levels_taught: List[int] = Field(..., min_items=1, description="Grades taught (10, 11, and/or 12)")
    email: Optional[str] = Field(None)


class TeacherUpdate(BaseSchema):
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None)
    institution_name: Optional[str] = Field(None, max_length=200)
    grade_levels_taught: Optional[List[int]] = Field(None)


class TeacherRead(BaseSchema):
    id: str
    username: str                   # = full_name
    full_name: str
    tsc_number: str
    institution_name: str
    grade_levels_taught: List[int]
    email: Optional[str]
    created_at: datetime