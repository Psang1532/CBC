from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    student_id: str = Field(
        ...,
        description="Government-issued unique student identifier"
    )


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int

    class Config:
        from_attributes = True
