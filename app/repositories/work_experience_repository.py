"""Persistence operations for work experience."""

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.work_experience import WorkExperience
from app.repositories.base_repository import BaseRepository


class WorkExperienceRepository(BaseRepository[WorkExperience]):
    """Persist and retrieve work-experience records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(WorkExperience, session)

    async def get_user_experience(self, user_id: UUID) -> list[WorkExperience]:
        """Return a user's experience records, most recent first."""
        result = await self.session.execute(
            select(WorkExperience).where(WorkExperience.user_id == user_id).order_by(WorkExperience.start_date.desc())
        )
        return list(result.scalars())

    async def current_jobs(self, user_id: UUID) -> list[WorkExperience]:
        """Return the user's current work-experience records."""
        result = await self.session.execute(
            select(WorkExperience).where(WorkExperience.user_id == user_id, WorkExperience.is_current.is_(True))
        )
        return list(result.scalars())

    async def total_years(self, user_id: UUID) -> float:
        """Return the sum of recorded work-experience durations in years."""
        experiences = await self.get_user_experience(user_id)
        today = date.today()
        return sum(((experience.end_date or today) - experience.start_date).days / 365.25 for experience in experiences)
