from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> List[ModelType]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        return obj

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
