"""Persistence operations for job applications."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import ApplicationStatus
from app.db.models.application import Application
from app.repositories.base_repository import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    """Persist and retrieve application records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Application, session)

    async def get_user_applications(self, user_id: UUID) -> list[Application]:
        """Return a user's applications, newest first."""
        result = await self.session.execute(
            select(Application).where(Application.user_id == user_id).order_by(Application.created_at.desc())
        )
        return list(result.scalars())

    async def get_job_applications(self, job_id: UUID) -> list[Application]:
        """Return applications for a job, newest first."""
        result = await self.session.execute(
            select(Application).where(Application.job_id == job_id).order_by(Application.created_at.desc())
        )
        return list(result.scalars())

    async def already_applied(self, user_id: UUID, job_id: UUID) -> bool:
        """Return whether a user has an application for a job."""
        return await self.exists(Application.user_id == user_id, Application.job_id == job_id)

    async def applications_by_status(self, status: ApplicationStatus) -> list[Application]:
        """Return applications with a particular status."""
        result = await self.session.execute(select(Application).where(Application.status == status))
        return list(result.scalars())
