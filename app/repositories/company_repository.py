"""Persistence operations for companies."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.company import Company
from app.db.models.industry import Industry
from app.repositories.base_repository import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    """Persist and retrieve company records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Company, session)

    async def get_by_name(self, name: str) -> Company | None:
        """Return a company by case-insensitive exact name."""
        result = await self.session.execute(select(Company).where(func.lower(Company.name) == name.lower()))
        return result.scalar_one_or_none()

    async def get_by_website(self, url: str) -> Company | None:
        """Return the company with the supplied website URL, if present."""
        result = await self.session.execute(select(Company).where(Company.website == url))
        return result.scalar_one_or_none()

    async def search(self, name: str) -> list[Company]:
        """Return companies whose names contain ``name``."""
        result = await self.session.execute(select(Company).where(Company.name.ilike(f"%{name.strip()}%")).order_by(Company.name))
        return list(result.scalars())

    async def companies_by_industry(self, industry: UUID | str) -> list[Company]:
        """Return companies for an industry ID or case-insensitive industry name."""
        statement = select(Company)
        if isinstance(industry, UUID):
            statement = statement.where(Company.industry_id == industry)
        else:
            statement = statement.join(Company.industry).where(func.lower(Industry.name) == industry.lower())
        result = await self.session.execute(statement.order_by(Company.name))
        return list(result.scalars())
