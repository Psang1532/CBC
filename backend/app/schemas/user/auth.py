from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None  # "student" or "teacher"


class RefreshTokenRequest(BaseModel):
    refresh_token: str