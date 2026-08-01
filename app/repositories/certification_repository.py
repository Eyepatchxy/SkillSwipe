"""Persistence operations for certifications."""

from datetime import date
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.certification import Certification
from app.repositories.base_repository import BaseRepository


class CertificationRepository(BaseRepository[Certification]):
    """Persist and retrieve certification records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Certification, session)

    async def get_user_certifications(self, user_id: UUID) -> list[Certification]:
        """Return a user's certifications, newest issue date first."""
        result = await self.session.execute(
            select(Certification).where(Certification.user_id == user_id).order_by(Certification.issue_date.desc())
        )
        return list(result.scalars())

    async def active_certifications(self, user_id: UUID) -> list[Certification]:
        """Return the user's certifications that have not expired."""
        result = await self.session.execute(
            select(Certification)
            .where(
                Certification.user_id == user_id,
                or_(Certification.expiry_date.is_(None), Certification.expiry_date >= date.today()),
            )
            .order_by(Certification.expiry_date.asc().nulls_last())
        )
        return list(result.scalars())

    async def expired_certifications(self) -> list[Certification]:
        """Return all certifications whose expiry date has passed."""
        result = await self.session.execute(
            select(Certification).where(Certification.expiry_date < date.today()).order_by(Certification.expiry_date)
        )
        return list(result.scalars())
