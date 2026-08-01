"""Persistence operations for saved jobs."""

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.saved_job import SavedJob
from app.repositories.base_repository import BaseRepository


class SavedJobRepository(BaseRepository[SavedJob]):
    """Persist and retrieve saved-job associations."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(SavedJob, session)

    async def saved_jobs(self, user_id: UUID) -> list[SavedJob]:
        """Return a user's saved-job associations, newest first."""
        result = await self.session.execute(
            select(SavedJob).where(SavedJob.user_id == user_id).order_by(SavedJob.created_at.desc())
        )
        return list(result.scalars())

    async def is_saved(self, user_id: UUID, job_id: UUID) -> bool:
        """Return whether a user has saved a job."""
        return await self.exists(SavedJob.user_id == user_id, SavedJob.job_id == job_id)

    async def remove_saved(self, user_id: UUID, job_id: UUID) -> bool:
        """Remove a saved job and report whether it existed."""
        result = await self.session.execute(
            delete(SavedJob).where(SavedJob.user_id == user_id, SavedJob.job_id == job_id)
        )
        return bool(result.rowcount)
