"""Persistence operations for education records."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.education import Education
from app.repositories.base_repository import BaseRepository


class EducationRepository(BaseRepository[Education]):
    """Persist and retrieve education records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Education, session)

    async def get_user_education(self, user_id: UUID) -> list[Education]:
        """Return a user's education records, most recent first."""
        result = await self.session.execute(
            select(Education).where(Education.user_id == user_id).order_by(Education.end_year.desc().nulls_last())
        )
        return list(result.scalars())

    async def highest_degree(self, user_id: UUID) -> Education | None:
        """Return the user's most recently completed degree record."""
        result = await self.session.execute(
            select(Education)
            .where(Education.user_id == user_id)
            .order_by(Education.end_year.desc().nulls_last(), Education.start_year.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
