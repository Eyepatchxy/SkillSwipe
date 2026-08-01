"""Persistence operations for jobs."""

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import JobStatus
from app.db.models.job import Job
from app.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository[Job]):
    """Persist and retrieve job records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Job, session)

    async def get_company_jobs(self, company_id: UUID) -> list[Job]:
        """Return jobs posted by a company, newest first."""
        result = await self.session.execute(select(Job).where(Job.company_id == company_id).order_by(Job.posted_date.desc()))
        return list(result.scalars())

    async def get_active_jobs(self) -> list[Job]:
        """Return currently open jobs, newest first."""
        result = await self.session.execute(select(Job).where(Job.status == JobStatus.OPEN).order_by(Job.posted_date.desc()))
        return list(result.scalars())

    async def search(self, filters: Mapping[str, Any]) -> list[Job]:
        """Return jobs matching supported title, location, and field filters."""
        statement = select(Job)
        query = filters.get("query") or filters.get("title")
        if isinstance(query, str) and query.strip():
            pattern = f"%{query.strip()}%"
            statement = statement.where(or_(Job.title.ilike(pattern), Job.description.ilike(pattern)))
        field_map = {
            "company_id": Job.company_id,
            "source_id": Job.source_id,
            "status": Job.status,
            "location": Job.location,
            "employment_type": Job.employment_type,
            "remote_type": Job.remote_type,
            "currency": Job.currency,
        }
        for field, column in field_map.items():
            value = filters.get(field)
            if value is not None:
                statement = statement.where(column == value)
        minimum_salary = filters.get("minimum_salary")
        if minimum_salary is not None:
            statement = statement.where(Job.max_salary >= minimum_salary)
        maximum_salary = filters.get("maximum_salary")
        if maximum_salary is not None:
            statement = statement.where(Job.min_salary <= maximum_salary)
        result = await self.session.execute(statement.order_by(Job.posted_date.desc()))
        return list(result.scalars())

    async def recent_jobs(self, limit: int) -> list[Job]:
        """Return up to ``limit`` most recently posted jobs."""
        result = await self.session.execute(select(Job).order_by(Job.posted_date.desc()).limit(limit))
        return list(result.scalars())

    async def jobs_by_location(self, location: str) -> list[Job]:
        """Return jobs matching a location case-insensitively."""
        result = await self.session.execute(select(Job).where(Job.location.ilike(f"%{location.strip()}%")).order_by(Job.posted_date.desc()))
        return list(result.scalars())

    async def jobs_by_source(self, source: UUID) -> list[Job]:
        """Return jobs imported from a source, newest first."""
        result = await self.session.execute(select(Job).where(Job.source_id == source).order_by(Job.posted_date.desc()))
        return list(result.scalars())
