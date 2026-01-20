# app/db/session.py
# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
#from contextlib import asynccontextmanager  
from app.settings import settings


# DO NOT create engine or sessionmaker at module level!

_engine = None
_async_session_maker = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            settings.database_url,
            echo=False,  # change to True for SQL logs during debug
            future=True,
        )
    return _engine


def get_async_session_maker():
    global _async_session_maker
    if _async_session_maker is None:
        _async_session_maker = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _async_session_maker

async def get_async_session() -> AsyncSession:
    """
    FastAPI dependency: provides a new async DB session per request.
    """
    maker = get_async_session_maker()
    async with maker() as session:
        yield session