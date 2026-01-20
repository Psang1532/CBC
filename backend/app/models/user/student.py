from typing import Optional

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Student(Base):
    __tablename__ = "students"

    username: Mapped[str] = mapped_column(
        String(100),            # longer to accommodate full names
        unique=True,
        index=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)   # same as username, for clarity
    student_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    institution_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    grade_level: Mapped[int] = mapped_column(Integer, nullable=False)     # 10, 11 or 12

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    # profile_picture_url: Mapped[Optional[str]] = ... (add later if needed)