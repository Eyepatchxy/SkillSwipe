"""Generic asynchronous persistence helpers."""

from typing import Any, Generic, TypeVar

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """Provide common asynchronous CRUD operations for an ORM model."""

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: Any) -> ModelType | None:
        """Return the model with the supplied primary key, if present."""
        result = await self.session.execute(select(self.model).where(self.model.id == id))  # type: ignore[attr-defined]
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        """Return all instances of the repository model."""
        result = await self.session.execute(select(self.model))
        return list(result.scalars())

    async def create(self, obj: ModelType) -> ModelType:
        """Add an object to the current unit of work."""
        self.session.add(obj)
        return obj

    async def delete_by_id(self, id: Any) -> bool:
        """Delete an object by primary key and report whether it existed."""
        result = await self.session.execute(delete(self.model).where(self.model.id == id))  # type: ignore[attr-defined]
        return bool(result.rowcount)

    async def delete(self, obj: ModelType) -> None:
        """Mark an object for deletion in the current unit of work."""
        await self.session.delete(obj)

    async def exists(self, *conditions: Any) -> bool:
        """Return whether an object matching all conditions exists."""
        result = await self.session.execute(select(self.model).where(*conditions))
        return result.scalar_one_or_none() is not None

    async def count(self) -> int:
        """Return the number of instances of the repository model."""
        result = await self.session.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def flush(self) -> None:
        """Flush pending changes without committing the transaction."""
        await self.session.flush()

    async def refresh(self, obj: ModelType) -> None:
        """Refresh an object from the database."""
        await self.session.refresh(obj)
