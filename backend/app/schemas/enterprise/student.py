from pydantic import Field

from app.schemas.base import BaseSchema


class StudentBase(BaseSchema):
    student_id: str = Field(
        ...,
        description="Government-issued unique student identifier"
    )


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: str
