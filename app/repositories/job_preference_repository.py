"""Persistence operations for job preferences."""

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.job_preference import JobPreference
from app.repositories.base_repository import BaseRepository


class JobPreferenceRepository(BaseRepository[JobPreference]):
    """Persist and retrieve job-preference records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(JobPreference, session)

    async def get_user_preferences(self, user_id: UUID) -> JobPreference | None:
        """Return the preferences configured for a user, if present."""
        result = await self.session.execute(select(JobPreference).where(JobPreference.user_id == user_id))
        return result.scalar_one_or_none()

    async def update_preferences(
        self, user_id: UUID, values: Mapping[str, Any] | None = None
    ) -> JobPreference | None:
        """Apply supplied allowed preference values and return the user's preferences."""
        preferences = await self.get_user_preferences(user_id)
        if preferences is None:
            return None
        allowed_fields = {
            "employment_type", "minimum_salary", "maximum_salary", "currency", "remote_preference",
            "requires_visa_sponsorship", "willing_to_relocate",
        }
        for field, value in (values or {}).items():
            if field in allowed_fields:
                setattr(preferences, field, value)
        return preferences
