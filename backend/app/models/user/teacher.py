from typing import List

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, List

from ..base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)   # same as username
    tsc_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    institution_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    grade_levels_taught: Mapped[List[int]] = mapped_column(JSONB, nullable=False, default=list)

    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)