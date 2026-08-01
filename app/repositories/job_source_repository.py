"""Persistence operations for job sources."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import SourceType
from app.db.models.job_source import JobSource
from app.repositories.base_repository import BaseRepository


class JobSourceRepository(BaseRepository[JobSource]):
    """Persist and retrieve job source records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(JobSource, session)

    async def get_enabled_sources(self) -> list[JobSource]:
        """Return configured sources that can be used to collect jobs."""
        result = await self.session.execute(select(JobSource).where(JobSource.status.in_([SourceType.SCRAPABLE, SourceType.FREEAPI, SourceType.PAIDAPI])))
        return list(result.scalars())

    async def get_scrapable_sources(self) -> list[JobSource]:
        """Return sources intended for scraping."""
        result = await self.session.execute(select(JobSource).where(JobSource.status == SourceType.SCRAPABLE))
        return list(result.scalars())

    async def get_paid_sources(self) -> list[JobSource]:
        """Return sources backed by paid APIs."""
        result = await self.session.execute(select(JobSource).where(JobSource.status == SourceType.PAIDAPI))
        return list(result.scalars())
