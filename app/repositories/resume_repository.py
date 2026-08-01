"""Persistence operations for resumes."""

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.resume import Resume
from app.repositories.base_repository import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    """Persist and retrieve resume records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Resume, session)

    async def get_default_resume(self, user_id: UUID) -> Resume | None:
        """Return the user's default resume, if one is configured."""
        result = await self.session.execute(
            select(Resume).where(Resume.user_id == user_id, Resume.is_default.is_(True))
        )
        return result.scalar_one_or_none()

    async def get_user_resumes(self, user_id: UUID) -> list[Resume]:
        """Return all resumes belonging to a user."""
        result = await self.session.execute(
            select(Resume).where(Resume.user_id == user_id).order_by(Resume.updated_at.desc())
        )
        return list(result.scalars())

    async def get_latest_resume(self, user_id: UUID) -> Resume | None:
        """Return the user's most recently updated resume."""
        result = await self.session.execute(
            select(Resume).where(Resume.user_id == user_id).order_by(Resume.updated_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def set_default(self, resume: Resume) -> Resume:
        """Make ``resume`` the only default resume for its owner."""
        await self.session.execute(
            update(Resume)
            .where(Resume.user_id == resume.user_id, Resume.id != resume.id, Resume.is_default.is_(True))
            .values(is_default=False)
        )
        resume.is_default = True
        return resume
