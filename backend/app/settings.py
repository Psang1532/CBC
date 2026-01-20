# app/settings.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:1532@db:5432/appdb"
    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        # Very helpful for debugging:
        case_sensitive=False,
        extra="ignore"     # ignore any other env vars that don't match fields
    )


# Create instance + print for immediate debug
settings = Settings()

# Add this temporary debug block – remove later
print("Loaded settings:")
print(f"  DATABASE_URL: {settings.database_url}")
print(f"  ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")