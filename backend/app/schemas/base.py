# app/schemas/base.py

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models.

    - Enables ORM compatibility
    - Safe to import everywhere
    - Contains NO domain logic
    """

    model_config = ConfigDict(
        from_attributes=True,   # allows reading from ORM objects
        populate_by_name=True,
        extra="forbid",  # reject unknown fields (recommended)
        str_strip_whitespace=True,
    )
